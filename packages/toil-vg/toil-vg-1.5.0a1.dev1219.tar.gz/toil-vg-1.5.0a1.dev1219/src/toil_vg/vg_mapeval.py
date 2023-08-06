#!/usr/bin/env python2.7
"""
vg_mapeval.py: Compare alignment positions from gam or bam to a truth set
that was created with vg sim --gam

"""
from __future__ import print_function
import argparse, sys, os, os.path, errno, random, subprocess, shutil, itertools, glob, tarfile
import doctest, re, json, collections, time, timeit
import logging, logging.handlers, SocketServer, struct, socket, threading
import string, math
import urlparse
import getpass
import pdb
import gzip
import logging
import copy
from collections import Counter

from math import ceil
from subprocess import Popen, PIPE

try:
    import numpy as np
    from sklearn.metrics import roc_auc_score, average_precision_score, r2_score, roc_curve
    have_sklearn = True
except:
    have_sklearn = False

import tsv

from toil.common import Toil
from toil.job import Job
from toil.realtimeLogger import RealtimeLogger
from toil_vg.vg_common import require, make_url, remove_ext,\
    add_common_vg_parse_args, add_container_tool_parse_args, get_vg_script, run_concat_lists, \
    parse_plot_sets, title_to_filename
from toil_vg.vg_map import map_parse_args, run_split_reads_if_needed, run_mapping
from toil_vg.vg_index import run_indexing, run_bwa_index
from toil_vg.context import Context, run_write_info_to_outstore

logger = logging.getLogger(__name__)

def mapeval_subparser(parser):
    """
    Create a subparser for mapeval.  Should pass in results of subparsers.add_parser()
    """

    # Add the Toil options so the job store is the first argument
    Job.Runner.addToilOptions(parser)
    
    # Add the out_store
    # TODO: do this at a higher level?
    # Or roll into Context?
    parser.add_argument('out_store',
                        help='output store.  All output written here. Path specified using same syntax as toil jobStore')
    
    # Add mapeval stuff
    add_mapeval_options(parser)
    
    # Add common docker options
    add_container_tool_parse_args(parser)
    
def add_mapeval_options(parser):
    """
    Add the mapeval options to the given argparse parser.
    """
    
    # General options
    parser.add_argument('--truth', type=make_url, default=None,
                        help='list of true positions of reads as output by toil-vg sim'
                        ' (by default positions extracted from --gam_input_reads or --bam_input_reads)')
    parser.add_argument('--skip-eval', action='store_true',
                        help='skip evaluation, ignore --truth, and just map reads')
    parser.add_argument('--gams', nargs='+', type=make_url, default=[],
                        help='aligned reads to compare to truth.  specify xg index locations with --index-bases')
    parser.add_argument("--index-bases", nargs='+', type=make_url, default=[],
                        help='use in place of gams to perform alignment.  will expect '
                        '<index-base>.gcsa, <index-base>.lcp and <index-base>.xg to exist.'
                        'Provide a comma-separated pair to use the first index for alignment and'
                        ' the second (.xg only) for annotation in the comparison')
    parser.add_argument('--use-gbwt', action='store_true',
                        help='also import <index-base>.gbwt and use it during alignment')
    parser.add_argument('--gbwt-penalties', nargs='+', type=float, default=[],
                        help='when using the GBWT, try all of the given recombination penalties instead of the default')
    parser.add_argument('--strip-gbwt', action='store_true',
                        help='run gbwt-free control runs')
    parser.add_argument('--use-snarls', action='store_true',
                        help='also import <index-base>.snarls and use it during multipath alignment')
    parser.add_argument('--vg-graphs', nargs='+', type=make_url, default=[],
                        help='vg graphs to use in place of gams or indexes.  indexes'
                        ' will be built as required')
    parser.add_argument('--gam-names', nargs='+', default=[],
                        help='a name for each gam passed in --gams/graphs/index-bases')
    parser.add_argument('--bams', nargs='+', type=make_url, default=[],
                        help='aligned reads to compare to truth in BAM format')
    parser.add_argument('--bam-names', nargs='+', default=[],
                        help='a name for each bam passed in with --bams')
    parser.add_argument('--pe-bams', nargs='+', type=make_url, default=[],
                        help='paired end aligned reads to compare to truth in BAM format')
    parser.add_argument('--pe-bam-names', nargs='+', default=[],
                        help='a name for each bam passed in with --pe-bams')
    parser.add_argument('--paired-only', action='store_true',
                        help='only do paired-end alignment (default is to do single and paired)')
    parser.add_argument('--single-only', action='store_true',
                        help='only do single-end alignment (default is to do single and paired)')
    
    parser.add_argument('--mapeval-threshold', type=int, default=200,
                        help='distance between alignment and true position to be called correct')

    parser.add_argument('--bwa', action='store_true',
                        help='run bwa mem on the reads, and add to comparison')
    parser.add_argument('--fasta', type=make_url, default=None,
                        help='fasta sequence file (required for bwa. if a bwa index exists for this file, it will be used)')
    parser.add_argument('--bwa-opts', type=str,
                        help='arguments for bwa mem (wrapped in \"\").')
    
    # We can compare all the scores against those from a particular GAM, if asked.
    parser.add_argument('--compare-gam-scores', default=None,
                        help='compare scores against those in the given named GAM')
                        
    parser.add_argument('--gbwt-baseline', default=None,
                        help='use GBWT scoring status in the given named GAM like snp1kg-gbwt5.0-mp-pe as a tag on all reads')
                        
    parser.add_argument('--downsample', type=float, default=None,
                        help='downsample alignment files to the given portion of reads for evaluation')

    parser.add_argument('--ignore-quals', action='store_true',
                        help='never use quality adjusted alignment. ' 
                        'necessary if using --multipath on reads not from trained simulator')

    parser.add_argument('--multipath-only', action='store_true',
                        help='run only mpmap and not map (--multipath will run both and using neither will just run map)')

    parser.add_argument('--more-mpmap-opts', nargs='+', default=[],
                        help='additional batches of mpmap options to try')

    parser.add_argument('--gam-input-xg', type=make_url, default=None,
                        help= 'If extracting truth positions from --gam_input_reads, specify corresponding xg for annotation')
                        
    parser.add_argument('--plot-sets', nargs='+', default=[],
                        help='comma-separated lists of condition-tagged GAM names (primary-mp-pe, etc.) with colon-separated title prefixes')
                        
    # We also need to have these options to make lower-level toil-vg code happy
    # with the options namespace we hand it.
    
    # Add mapping options
    map_parse_args(parser)
    
    # Add common options shared with everybody
    add_common_vg_parse_args(parser)
    
def get_default_mapeval_options():
    """
    Return an argparse Namespace populated with the default mapeval option
    values.
    
    Requires the required positional truth file argument.
    
    Can be modified and then passed to make_mapeval_plan(), so you can use
    mapeval as part of a larger program.
    
    """
    
    # Make a parser
    parser = argparse.ArgumentParser()
    # Stick our arguments on it
    add_mapeval_options(parser)
    # And parse nothing but mandatory arguments
    return parser.parse_args([])
    
def validate_options(options):
    """
    Throw an error if an invalid combination of options has been selected.
    """

    # We can only deal with one source of unaligned input reads
    input_count = sum(map(lambda x : x is not None, [options.gam_input_reads, options.bam_input_reads, options.fastq]))
    require(input_count <= 1,
            'no more than one of --gam_input_reads, --fastq, or --bam_input_reads allowed for input')
    
    # need to have input reads coming from somewhere
    require(options.gams != [] or input_count > 0,
            'either --gams must be specified with pre-aligned GAM files, or one of ' +
            '--gam_input_reads, --fastq, or --bam_input_reads must give reads to align')
            
    # Note that we have to accept --gams along with unaligned reads; in that
    # case we ignore the unaligned reads and use the pre-aligned GAMs.

    # annotation is not an option when reading fastq and doing evaluation
    require(not options.fastq or (options.truth or options.skip_eval),
            '--truth (or --skip-eval) required with --fastq input')

    # only one or two fastqs accepted
    require(not options.fastq or len(options.fastq) in [1,2],
            'only 1 or two fastqs accepted with --fatsq')

    # only gzipped fastqs accpeted
    require(not options.fastq or all(map(lambda x : x.endswith('.gz'), options.fastq)),
            'only gzipped fastqs (ending with .gz) accepted by --fastq')
            
    # check bwa / bam input parameters.  
    if options.bwa:
        require(options.fasta, '--fasta required for bwa')
    if options.bams:
        require(options.bam_names and len(options.bams) == len(options.bam_names),
                 '--bams and --bam-names must have same number of inputs')
    if options.pe_bams:
        require(options.pe_bam_names and len(options.pe_bams) == len(options.pe_bam_names),
                 '--pe-bams and --pe-bam-names must have same number of inputs')

    # some options from toil-vg map are disabled on the command line
    # this can be eventually cleaned up a bit better 
    require(not options.interleaved,
            '--interleaved disabled in toil-vg mapeval; a single --fastq is always assumed interleaved and two are always assumed paired')

    # accept graphs or indexes in place of gams
    require(options.gams or options.index_bases or options.vg_graphs,
            'one of --vg-graphs, --index-bases or --gams must be used to specifiy vg input')

    if options.use_gbwt:
        require(not options.gams,
                '--use-gbwt cannot be used with pre-aligned GAMs in --gams')
                
    require(not options.gbwt_penalties or options.use_gbwt,
            '--gbwt-penalties requires --use-gbwt')
            
    require(not options.gbwt_penalties or len(set(options.gbwt_penalties)) == len(options.gbwt_penalties),
            '--gbwt-penalties valuses must be unique')
                
    if options.use_snarls:
        require(options.multipath or options.multipath_only,
                '--use-snarls only affects the multipath mapper (--multipath or --multipath-only)')

    if options.gams:
        require(len(options.index_bases) == len(options.gams),
                '--index-bases must be used along with --gams to specify xg locations')
    if options.vg_graphs:
        require(not options.gams and not options.index_bases,
                'if --vg-graphs specified, --gams and --index-bases must not be used')

    # must have a name for each graph/index/gam
    if options.gams:
        require(options.gam_names and len(options.gams) == len(options.gam_names),
                 '--gams and --gam_names must have same number of inputs')
    if options.vg_graphs:
        require(options.gam_names and len(options.vg_graphs) == len(options.gam_names),
                 '--vg-graphs and --gam_names must have same number of inputs')
    if options.index_bases:
        require(options.gam_names and len(options.index_bases) == len(options.gam_names),
                 '--index-bases and --gam_names must have same number of inputs')
                 
    # Make sure names are unique so we can use them as dict keys and file names
    names = []
    if options.bam_names:
        names += options.bam_names
    if options.pe_bam_names:
        names += options.pe_bam_names
    if options.gam_names:
        names += options.gam_names
    require(len(names) == len(set(names)), 'all names must be unique')

    require(options.gam_input_reads is None or options.bam_input_reads is None,
            '--gam_input_reads and --bam_input_reads cannot both be specified')

    require(options.truth or options.skip_eval or options.bam_input_reads or options.gam_input_xg,
            '--gam-input-xg must be provided to annotate reads, or reads must be input in BAM format or with associated truth')
            
    # We can't downsample with GAM baseline because we still aren't properly deterministic for some reason.
    # TODO: fix that
    require(options.gbwt_baseline is None or options.downsample is None or options.downsample == 1.0,
            '--gam-baseline cannot be used with --downsample until downsampling is properly deterministic')
    
def parse_int(value):
    """
    Parse an int, interpreting an empty string as 0.
    """
    
    return int(value) if value.strip() != '' else 0

def run_bam_to_fastq(job, context, bam_file_id, paired_mode, add_paired_suffix=False):
    """
    convert a bam to fastq (or pair of fastqs).  add_suffix will stick a _1 or _2 on
    paired reads (needed for vg, but not bwa)
    """
    work_dir = job.fileStore.getLocalTempDir()

    # read the bam file
    bam_file = os.path.join(work_dir, 'input.bam')
    job.fileStore.readGlobalFile(bam_file_id, bam_file)
    
    # if we're paired, must make some split files
    if paired_mode:
        sim_fq_files = [os.path.join(work_dir, 'sim_1{}.fq'.format('s' if add_paired_suffix else '')),
                        os.path.join(work_dir, 'sim_2{}.fq'.format('s' if add_paired_suffix else ''))]
        cmd = ['samtools', 'fastq', os.path.basename(bam_file),
               '-1', os.path.basename(sim_fq_files[0]),
               '-2', os.path.basename(sim_fq_files[1])]
        if add_paired_suffix:
            cmd += ['-N']
        else:
            cmd += ['-n']
        context.runner.call(job, cmd, work_dir = work_dir)
        # we change /1 /2 --> _1 _2 to be compatible with rest of mapeval
        gzip_cmd = [['sed', os.path.basename(sim_fq_files[0]), '-e', 's/\/1/_1/g'], ['gzip', '-c']]
        with open(sim_fq_files[0] + '.gz', 'w') as gz_file:
            context.runner.call(job, gzip_cmd, work_dir = work_dir, outfile = gz_file)
        gzip_cmd = [['sed', os.path.basename(sim_fq_files[1]), '-e', 's/\/2/_2/g'], ['gzip', '-c']]
        with open(sim_fq_files[1] + '.gz', 'w') as gz_file:
            context.runner.call(job, gzip_cmd, work_dir = work_dir, outfile = gz_file)
        return [context.write_intermediate_file(job, sim_fq_files[0] + '.gz'),
                context.write_intermediate_file(job, sim_fq_files[1] + '.gz')]
    else:
        sim_fq_file = os.path.join(work_dir, 'sim.fq.gz')
        cmd = [['samtools', 'fastq', os.path.basename(bam_file), '-N']]
        # we change /1 /2 --> _1 _2 to be compatible with rest of mapeval
        cmd.append(['sed', '-e', 's/\/1/_1/g', '-e', 's/\/2/_2/g'])
        cmd.append(['gzip'])
        with open(sim_fq_file, 'w') as sim_file:
            context.runner.call(job, cmd, work_dir = work_dir, outfile = sim_file)
        return [context.write_intermediate_file(job, sim_fq_file)]
    
def run_gam_to_fastq(job, context, gam_file_id, paired_mode,
                     add_paired_suffix=False, out_name = 'sim', out_store = False, ):
    """
    convert a gam to fastq (or pair of fastqs)
    """
    work_dir = job.fileStore.getLocalTempDir()

    # read the gam file
    gam_file = os.path.join(work_dir, 'input.gam')
    job.fileStore.readGlobalFile(gam_file_id, gam_file)

    write_fn = context.write_output_file if out_store else context.write_intermediate_file
    
    # if we're paired, must make some split files
    if paired_mode:
        # convert to json (todo: have docker image that can do vg and jq)
        json_file = gam_file + '.json'
        cmd = ['vg', 'view', '-a', os.path.basename(gam_file)]
        with open(json_file, 'w') as out_json:
            context.runner.call(job, cmd, work_dir = work_dir, outfile = out_json)

        sim_fq_files = [None, os.path.join(work_dir, '{}_1{}.fq.gz'.format(out_name, 's' if add_paired_suffix else '')),
                        os.path.join(work_dir, '{}_2{}.fq.gz'.format(out_name, 's' if add_paired_suffix else ''))]

        # make a fastq for each end of pair
        for i in [1, 2]:
            # extract paired end with jq
            cmd = ['jq', '-cr', 'select(.name | test("_{}$"))'.format(i),
                   os.path.basename(json_file)]
            end_file = json_file + '.{}'.format(i)
            with open(end_file, 'w') as end_out:
                context.runner.call(job, cmd, work_dir = work_dir, outfile = end_out)

            cmd = [['vg', 'view', '-JaG', os.path.basename(end_file)]]
            cmd.append(['vg', 'view', '-X', '-'])
            if not add_paired_suffix:
                cmd.append(['sed', 's/_{}$//'.format(i)])
            cmd.append(['gzip'])

            with open(sim_fq_files[i], 'w') as sim_out:
                context.runner.call(job, cmd, work_dir = work_dir, outfile = sim_out)

            os.remove(end_file)

        return [write_fn(job, sim_fq_files[1]), write_fn(job, sim_fq_files[2])]
            
    else:
        # extract reads from gam.  as above, need to have single docker container (which shouldn't be
        # a big deal) to run all these chained command and avoid huge files on disk
        extracted_reads_file = os.path.join(work_dir, '{}.fq.gz'.format(out_name))
        cmd = [['vg', 'view', '-X', os.path.basename(gam_file)]]
        cmd.append(['gzip'])
        with open(extracted_reads_file, 'w') as out_ext:
            context.runner.call(job, cmd, work_dir = work_dir, outfile = out_ext)

        return [write_fn(job, extracted_reads_file)]

def run_concat_fastqs(job, context, fq_reads_ids):
    """ concatenate some fastq files
    """
    work_dir = job.fileStore.getLocalTempDir()

    assert len(fq_reads_ids) == 2
    # read the reads
    fq_file_names = [os.path.join(work_dir, 'reads-{}.fq.gz'.format(i)) \
                     for i in range(len(fq_reads_ids))]
    for fq_id, fq_name in zip(fq_reads_ids, fq_file_names):
        job.fileStore.readGlobalFile(fq_id, fq_name, mutable=fq_name==fq_file_names[0])

    # concat the reads (should work fine for gzipped or not)
    with open(fq_file_names[0], 'a') as out_file:
        for fq_name in fq_file_names[1:]:
            with open(fq_name) as fq_file:
                shutil.copyfileobj(fq_file, out_file)

    return context.write_intermediate_file(job, fq_file_names[0])

def run_strip_fq_ext(job, context, fq_reads_ids):
    """ bwa can't read reads with _1 _2 extensions for paired end alignment.  strip here
    """
    
    work_dir = job.fileStore.getLocalTempDir()

    # read the reads
    fq_file_names = [os.path.join(work_dir, 'reads-{}.fq.gz'.format(i)) \
                     for i in range(len(fq_reads_ids))]
    out_file_names = [os.path.join(work_dir, 'reads-strip-{}.fq.gz'.format(i)) \
                      for i in range(len(fq_reads_ids))]
    out_ids = []
    
    for fq_id, fq_name,  out_name in zip(fq_reads_ids, fq_file_names, out_file_names):
        job.fileStore.readGlobalFile(fq_id, fq_name, mutable=fq_name==fq_file_names[0])
        cmd = [['pigz', '-dc', os.path.basename(fq_name)]]
        cmd.append(['sed', '-e', 's/_1$\|_2$//g'])
        cmd.append(['pigz', '-c', '-p', str(max(1, job.cores))])
        with open(out_name, 'w') as out_file:
            context.runner.call(job, cmd, work_dir = work_dir, outfile = out_file)
        out_ids.append(context.write_intermediate_file(job, out_name))

    return out_ids
    
def run_bwa_mem(job, context, fq_reads_ids, bwa_index_ids, paired_mode):
    """ run bwa-mem on reads in a fastq.  optionally run in paired mode
    return id of bam file
    """

    # We need to compute the total size of our inputs, expected intermediates,
    # and outputs, and re-queue ourselves if we don't have enough disk.
    required_disk = 0
    for fastq_id in fq_reads_ids:
        # We need all the FASTQs downloaded
        required_disk += fastq_id.size
        
    # Say we need room for the aligned BAM, and the intermediate SAM file.
    # TODO: Is this factor sufficient?
    required_disk *= 8
    
    for idx_id in bwa_index_ids.values():
        # We also need room for the indexes
        required_disk += idx_id.size
    
    # Add some padding
    required_disk += 1024 ** 3
        
    if job.disk < required_disk:
        # Re-queue with more disk
        RealtimeLogger.info("Re-queueing run_bwa_mem with {} bytes of disk; originally had {}".format(required_disk, job.disk))
        requeued = job.addChildJobFn(run_bwa_mem, context, fq_reads_ids, bwa_index_ids, paired_mode,
            cores=job.cores, memory=job.memory,
            disk=required_disk)
        return requeued.rv()
            

    work_dir = job.fileStore.getLocalTempDir()

    # read the reads
    fq_file_names = []
    for i, fq_reads_id in enumerate(fq_reads_ids):
        fq_file_names.append(os.path.join(work_dir, 'reads{}.fq.gz'.format(i)))
        job.fileStore.readGlobalFile(fq_reads_id, fq_file_names[-1])

    # and the index files
    fasta_file = os.path.join(work_dir, 'reference.fa')
    for suf, idx_id in bwa_index_ids.items():
        job.fileStore.readGlobalFile(idx_id, '{}{}'.format(fasta_file, suf))

    # output positions file
    bam_file = os.path.join(work_dir, 'bwa-mem')
    if paired_mode:
        bam_file += '-pe'
    bam_file += '.bam'
    
    # if we're paired, must make some split files
    if paired_mode:

        # run bwa-mem on the paired end input
        start_time = timeit.default_timer()
        cmd = ['bwa', 'mem', '-t', str(context.config.alignment_cores), os.path.basename(fasta_file),
                os.path.basename(fq_file_names[0])]
        if len(fq_file_names) == 2:
            cmd += [os.path.basename(fq_file_names[1])]
        else:
            # if one file comes in, it had better be interleaved
            cmd += ['-p']
        cmd += context.config.bwa_opts
        
        with open(bam_file + '.sam', 'w') as out_sam:
            context.runner.call(job, cmd, work_dir = work_dir, outfile = out_sam)

        end_time = timeit.default_timer()
        run_time = end_time - start_time

        # we take care to mimic output message from vg_map.py, so we can mine them both for the jenkins
        # report        
        RealtimeLogger.info("Aligned aligned-linear_0.gam. Process took {} seconds with paired-end bwa-mem".format(
            run_time))
            
        # separate samtools for docker (todo find image with both)
        # 2304 = get rid of 256 (secondary) + 2048 (supplementary)        
        cmd = ['samtools', 'view', '-1', '-F', '2304', os.path.basename(bam_file + '.sam')]
        with open(bam_file, 'w') as out_bam:
            context.runner.call(job, cmd, work_dir = work_dir, outfile = out_bam)

    # single end
    else:
        assert len(fq_file_names) == 1

        # run bwa-mem on single end input
        start_time = timeit.default_timer()
        cmd = ['bwa', 'mem', '-t', str(context.config.alignment_cores), os.path.basename(fasta_file),
                os.path.basename(fq_file_names[0])] + context.config.bwa_opts

        with open(bam_file + '.sam', 'w') as out_sam:
            context.runner.call(job, cmd, work_dir = work_dir, outfile = out_sam)

        end_time = timeit.default_timer()
        run_time = end_time - start_time

        # we take care to mimic output message from vg_map.py, so we can mine them both for the jenkins
        # report
        RealtimeLogger.info("Aligned aligned-linear_0.gam. Process took {} seconds with single-end bwa-mem".format(
            run_time))            

        # separate samtools for docker (todo find image with both)
        # 2304 = get rid of 256 (secondary) + 2048 (supplementary)
        cmd = ['samtools', 'view', '-1', '-F', '2304', os.path.basename(bam_file + '.sam')]
        with open(bam_file, 'w') as out_bam:
            context.runner.call(job, cmd, work_dir = work_dir, outfile = out_bam)


    # return our id for the output bam file
    bam_file_id = context.write_output_file(job, bam_file)

    return bam_file_id, run_time
    
def downsample_bam(job, context, bam_file_id, fraction):
    """
    Extract the given fraction of reads from the given BAM file. Return the
    file ID for the new BAM file.
    """
    
    work_dir = job.fileStore.getLocalTempDir()
    
    in_file = os.path.join(work_dir, 'full.bam')
    out_file = os.path.join(work_dir, 'downsampled.bam')
    
    job.fileStore.readGlobalFile(bam_file_id, in_file)
    
    cmd = ['samtools', 'view', '-b', '-s', str(fraction), os.path.basename(in_file)]
    with open(out_file, 'w') as out_bam:
        context.runner.call(job, cmd, work_dir = work_dir, outfile = out_bam)
        
    return context.write_intermediate_file(job, out_file)
    
def downsample_gam(job, context, gam_file_id, fraction):
    """
    Extract the given fraction of reads from the given GAM file. Return the
    file ID for the new GAM file.
    """
    
    work_dir = job.fileStore.getLocalTempDir()
    
    in_file = os.path.join(work_dir, 'full.gam')
    out_file = os.path.join(work_dir, 'downsampled.gam')
    
    job.fileStore.readGlobalFile(gam_file_id, in_file)
    
    cmd = ['vg', 'filter', '-t', str(job.cores), '--downsample', str(fraction), os.path.basename(in_file)]
    with open(out_file, 'w') as out_gam:
        context.runner.call(job, cmd, work_dir = work_dir, outfile = out_gam)
        
    return context.write_intermediate_file(job, out_file)
    

def extract_bam_read_stats(job, context, name, bam_file_id, paired, sep='_'):
    """
    extract positions, scores, and MAPQs from bam, return id of read stats file
    (lots of duplicated code with vg_sim, should merge?)
    
    Produces a read stats TSV of the format:
    read name, read tags (or '.'), [contig aligned to, alignment position,]* score, MAPQ
    
    TODO: Currently scores are not extracted and a score of 0 is always
    returned.
    
    TODO: Tags are also always '.'.

    """

    work_dir = job.fileStore.getLocalTempDir()

    # download input
    bam_file = os.path.join(work_dir, name)
    job.fileStore.readGlobalFile(bam_file_id, bam_file)

    out_pos_file = bam_file + '.tsv'

    # 2304 = get rid of 256 (secondary) + 2048 (supplementary)        
    cmd = [['samtools', 'view', os.path.basename(bam_file), '-F', '2304']]
    cmd.append(['grep', '-v', '^@'])
    if paired:
        # Now we use inline perl to parse the SAM flags and synthesize TSV
        # TODO: will need to switch to something more powerful to parse the score out of the AS tag. For now score everything as 0.
        # TODO: why _ and not / as the read name vs end number delimiter?
        # Note: we are now adding length/2 to the positions to be more consistent with vg annotate
        cmd.append(['perl', '-ne', '@val = split("\t", $_); print @val[0] . "{}" . (@val[1] & 64 ? "1" : @val[1] & 128 ? "2" : "?"), "\t.\t" . @val[2] . "\t" . (@val[3] +  int(length(@val[9]) / 2)) . "\t0\t" . @val[4] . "\n";'.format(sep)])
    else:
        # No flags to parse since there's no end pairing and read names are correct.
        # Use inline perl again and insert a fake 0 score column
        # Note: we are now adding length/2 to the positions to be more consistent with vg annotate        
        cmd.append(['perl', '-ne', '@val = split("\t", $_); print @val[0] . "\t.\t" . @val[2] . "\t" . (@val[3] +  int(length(@val[9]) / 2)) . "\t0\t" . @val[4] . "\n";'])
    cmd.append(['sort'])
    
    with open(out_pos_file, 'w') as out_pos:
        context.runner.call(job, cmd, work_dir = work_dir, outfile = out_pos)

    stats_file_id = context.write_intermediate_file(job, out_pos_file)
    return stats_file_id

    
def annotate_gam(job, context, xg_file_id, gam_file_id):
    """
    Annotate the given GAM file with positions from the given XG file.
    """
    
    work_dir = job.fileStore.getLocalTempDir()

    # download input
    RealtimeLogger.info('Download XG from file {}'.format(xg_file_id))
    xg_file = os.path.join(work_dir, 'index.xg')
    job.fileStore.readGlobalFile(xg_file_id, xg_file)
    gam_file = os.path.join(work_dir, 'reads.gam')
    job.fileStore.readGlobalFile(gam_file_id, gam_file)
    
    annotated_gam_file = os.path.join(work_dir, 'annotated.gam')
    
    cmd = [['vg', 'annotate', '-p', '-a', os.path.basename(gam_file), '-x', os.path.basename(xg_file)]]
    with open(annotated_gam_file, 'w') as out_file:
        try:
            context.runner.call(job, cmd, work_dir=work_dir, outfile=out_file)
        except:
            # Dump everything we need to replicate the annotation call
            logging.error("GAM annotation failed. Dumping files.")
            context.write_output_file(job, gam_file)
            context.write_output_file(job, xg_file)
            raise
    
    return context.write_intermediate_file(job, annotated_gam_file)
    
    
def extract_gam_read_stats(job, context, name, gam_file_id, generate_tags=[]):
    """
    extract positions, scores, and MAPQs for reads from a gam, and return the id
    of the resulting read stats file
    
    The read stats file may also be used as a truth file; the two kinds of files are the same format.
    
    Produces a read stats TSV of the format:
    read name, read tags (or '.'), [contig aligned to, alignment position,]* score, MAPQ
    
    If generate_tags is specified, it is a list of boolean GAM annotation names
    that will be turned into tags, in addition to the contents of the features
    annotation.
    
    If the GAM is not annotated with alignment positions, contig and position
    will both contain only "0" values.

    """

    work_dir = job.fileStore.getLocalTempDir()

    gam_file = os.path.join(work_dir, name)
    job.fileStore.readGlobalFile(gam_file_id, gam_file)

    out_pos_file = gam_file + '.tsv'
                           
    # go through intermediate json file until docker worked out
    gam_annot_json = gam_file + '.json'
    cmd = [['vg', 'view', '-aj', os.path.basename(gam_file)]]
    with open(gam_annot_json, 'w') as output_annot_json:
        context.runner.call(job, cmd, work_dir = work_dir, outfile=output_annot_json)
        
    # Write jq code to generate additional tags
    tag_generation = ''
    for annotation_name in generate_tags:
        # If the annotation exists with a truthy value, add a feature with the annotation name, which will become a tag.
        tag_generation += ('.annotation.features = (if (.annotation.features | length) > 0 then .annotation.features else [] end + ' +
            'if .annotation.' + annotation_name + ' then ["' + annotation_name + '"] else [] end) | ')

    # turn the annotated gam json into truth positions, as separate command since
    # we're going to use a different docker container.  (Note, would be nice to
    # avoid writing the json to disk)
    # TODO: Deduplicate this code with the truth file generation code in vg_sim.py!
    jq_cmd = ['jq', '-c', '-r', tag_generation + '[.name] + '
              'if (.annotation.features | length) > 0 then [.annotation.features | join(",")] else ["."] end + '
              'if .refpos != null then [.refpos[] | .name, if .offset != null then .offset else 0 end] else [] end + '
              '[.score] + '
              'if .mapping_quality == null then [0] else [.mapping_quality] end | @tsv',
              os.path.basename(gam_annot_json)]
    # convert back to _1 format (only relevant if running on bam input reads where / added automatically)
    jq_pipe = [jq_cmd, ['sed', '-e', 's/null/0/g',  '-e', 's/\/1/_1/g', '-e', 's/\/2/_2/g']]
    with open(out_pos_file + '.unsorted', 'w') as out_pos:
        context.runner.call(job, jq_pipe, work_dir = work_dir, outfile=out_pos)

    # get rid of that big json asap
    os.remove(gam_annot_json)

    # sort the read stats file (not piping due to memory fears)
    sort_cmd = ['sort', os.path.basename(out_pos_file) + '.unsorted']
    with open(out_pos_file, 'w') as out_pos:
        context.runner.call(job, sort_cmd, work_dir = work_dir, outfile = out_pos)

    # Some lines may have refpos set while others do not (and those columns may be absent)

    out_stats_file_id = context.write_intermediate_file(job, out_pos_file)
    return out_stats_file_id
    
def compare_positions(job, context, truth_file_id, name, stats_file_id, mapeval_threshold):
    """
    Compares positions from two TSV files. Both files have the format:
    read name, comma-separated tag list (or '.'), [contig touched, true position]*, score, MAPQ
    
    The truth file will have the base tag list, while the stats file will
    have the cannonical score and MAPQ, as well as additional tags to add.
    
    The input files must be in lexicographically sorted order by name, but may
    not contain the same number of entries each. The stats file may be a subset
    of the truth.
    
    Produces a TSV of the form:
    read name, correctness flag (0/1), MAPQ, comma-separated tag list (or '.')

    Returns output file ID.
    
    mapeval_threshold is the distance within which a mapping is held to have hit
    the correct position.

    TODO: Replace with a vg mapeval call.
    
    """
    work_dir = job.fileStore.getLocalTempDir()

    true_read_stats_file = os.path.join(work_dir, 'true.tsv')
    job.fileStore.readGlobalFile(truth_file_id, true_read_stats_file)
    test_read_stats_file = os.path.join(work_dir, name + '.tsv')
    job.fileStore.readGlobalFile(stats_file_id, test_read_stats_file)

    out_file = os.path.join(work_dir, name + '.compare.positions')

    with open(true_read_stats_file) as truth, open(test_read_stats_file) as test, open(out_file, 'w') as out_stream:
        out = tsv.TsvWriter(out_stream)
        
        # Make readers for the files
        truth_reader = iter(tsv.TsvReader(truth))
        test_reader = iter(tsv.TsvReader(test))
        
        # Start an iteration over them
        true_fields = next(truth_reader, None)
        test_fields = next(test_reader, None)
        
        # Track line numbers for error reporting
        true_line = 1
        test_line = 1
        
        while true_fields is not None and test_fields is not None:
            # We still have data on both sides
            
            # The minimum field count you can have for the truth is 6, because it must have at least one position.
            # For the test data it can be 4, because the read may have no positions.
            
            if len(true_fields) < 6:
                raise RuntimeError('Incorrect (<6) true field count on line {}: {}'.format(
                    true_line, true_fields))
            
            if len(test_fields) < 4:
                raise RuntimeError('Incorrect (<4) test field count on line {}: {}'.format(
                    test_line, test_fields))
            
            true_read_name = true_fields[0]
            aln_read_name = test_fields[0]
            
            if true_read_name < aln_read_name:
                # We need to advance the true read
                true_fields = next(truth_reader, None)
                true_line += 1
                # Make sure we went forward
                assert(true_fields == None or true_fields[0] > true_read_name)
                continue
            elif aln_read_name < true_read_name:
                # We need to advance the aligned read
                test_fields = next(test_reader, None)
                test_line += 1
                # Make sure we went forward
                assert(test_fields == None or test_fields[0] > aln_read_name)
                continue
            else:
                # The reads correspond. Check if the positions are right.
                
                assert(aln_read_name == true_read_name)

                # Grab the comma-separated tags from the truth file.
                aln_tags = true_fields[1]
                if aln_tags == '':
                    aln_tags = '.'
                
                # The test file also has a tag slot for additional tags
                aln_extra_tags = test_fields[1]
                if aln_extra_tags == '':
                    aln_extra_tags = '.'
                    
                # Combine the tags into a set of all observed tags
                combined_tags = set(aln_tags.split(',')) | set(aln_extra_tags.split(','))
                # Except the no-tags '.' if present
                combined_tags -= {'.'}
                
                # Make into a string again
                combined_tags_string = ','.join(sorted(combined_tags)) if len(combined_tags) > 0 else '.'
                
                # map seq name->position
                # Grab everything after the tags column and before the score and mapq columns, in pairs.
                true_pos_dict = dict(zip(true_fields[2:-2:2], map(parse_int, true_fields[3:-2:2])))
                aln_pos_dict = dict(zip(test_fields[2:-2:2], map(parse_int, test_fields[3:-2:2])))
                
                # Make sure the true reads came from somewhere
                assert(len(true_pos_dict) > 0)
                
                # Skip over score field and get the MAPQ, which is last
                aln_mapq = parse_int(test_fields[-1])
                aln_correct = 0
                for aln_chr, aln_pos in aln_pos_dict.items():
                    if aln_chr in true_pos_dict and abs(true_pos_dict[aln_chr] - aln_pos) < mapeval_threshold:
                        aln_correct = 1
                        break

                out.line(aln_read_name, aln_correct, aln_mapq, combined_tags_string)
        
                # Advance both reads
                true_fields = next(truth_reader, None)
                true_line += 1
                test_fields = next(test_reader, None)
                test_line += 1
        
    out_file_id = context.write_intermediate_file(job, out_file)
    return out_file_id
    
def compare_scores(job, context, baseline_name, baseline_file_id, name, score_file_id):
    """ Compares scores from TSV files. The baseline and file under test both
    have the format: read name, contig aligned to, alignment position,
    alignment score, MAPQ
    
    Both must be in lexicographical order by read name, but they need not have
    the same length. The score file may be a subset of the baseline.
    
    Produces a CSV (NOT TSV) of the form: read name, score difference, aligned
    score, baseline score
    
    If saved to the out store it will be: <condition name>.compare.<baseline
    name>.scores
    
    Uses the given (condition) name as a file base name for the file under
    test.
    
    """
    work_dir = job.fileStore.getLocalTempDir()

    baseline_read_stats_file = os.path.join(work_dir, 'baseline.tsv')
    job.fileStore.readGlobalFile(baseline_file_id, baseline_read_stats_file)
    test_read_stats_file = os.path.join(work_dir, name + '.tsv')
    job.fileStore.readGlobalFile(score_file_id, test_read_stats_file)

    out_file = os.path.join(work_dir, '{}.compare.{}.scores'.format(name, baseline_name))

    with open(baseline_read_stats_file) as baseline, open(test_read_stats_file) as test, open(out_file, 'w') as out:
        
        # Make readers for the files
        baseline_reader = iter(tsv.TsvReader(baseline))
        test_reader = iter(tsv.TsvReader(test))
        
        # Start an iteration over them
        baseline_fields = next(baseline_reader, None)
        test_fields = next(test_reader, None)
        
        # Track line numbers for error reporting
        baseline_line = 1
        test_line = 1
        
        while baseline_fields is not None and test_fields is not None:
            # We still have data on both sides
            
            if len(baseline_fields) < 5:
                raise RuntimeError('Incorrect (<5) baseline field count on line {}: {}'.format(
                    baseline_line, baseline_fields))
            
            if len(test_fields) < 5:
                raise RuntimeError('Incorrect (<5) test field count on line {}: {}'.format(
                    test_line, test_fields))
            
            baseline_read_name = baseline_fields[0]
            aln_read_name = test_fields[0]
            
            if baseline_read_name < aln_read_name:
                # We need to advance the baseline read
                baseline_fields = next(baseline_reader, None)
                baseline_line += 1
                continue
            elif aln_read_name < baseline_read_name:
                # We need to advance the aligned read
                test_fields = next(test_reader, None)
                test_line += 1
                continue
            else:
                # The reads correspond. Check if the positions are right.
                
                # Order is: name, conting, pos, score, mapq
                aligned_score = test_fields[-2]
                baseline_score = baseline_fields[-2]
                # Compute the score difference. Scores are integers.
                score_diff = parse_int(aligned_score) - parse_int(baseline_score)
                
                # Report the score difference            
                out.write('{}, {}, {}, {}\n'.format(baseline_fields[0], score_diff, aligned_score, baseline_score))

                # Advance both reads
                baseline_fields = next(baseline_reader, None)
                baseline_line += 1
                test_fields = next(test_reader, None)
                test_line += 1
                
    # Save stats file for inspection
    out_file_id = context.write_intermediate_file(job, out_file)
        
    return out_file_id

def run_map_eval_index(job, context, xg_file_ids, gcsa_file_ids, gbwt_file_ids, id_range_file_ids, snarl_file_ids, vg_file_ids):
    """ 
    Index the given vg files.
    
    If no vg files are provided, pass through the given indexes. Indexes are
    lists of index IDs, one per graph, except gcsa_file_ids, which is tuples of
    GCSA and LCP file IDs, one tuple per graph. Index types which are not used
    should have falsey values instead of lists.
    
    Returns a list of dicts from index type name to index file ID, as used by
    run_indexing in vg_index.py, holding file IDs for different index
    components.
    
    """

    # index_ids are dicts from index type to file ID as returned by run_indexing
    index_ids = []
    if vg_file_ids:
        for vg_file_id in vg_file_ids:
            index_job = job.addChildJobFn(run_indexing, context, [vg_file_id], ['default.vg'],
                                          'index', ['default'], 
                                          cores=context.config.misc_cores, memory=context.config.misc_mem,
                                          disk=context.config.misc_disk)
            index_ids.append(index_job.rv())
    else:
        for i, xg_id in enumerate(xg_file_ids):
            # For each graph, gather and tag its indexes
            indexes = {}
            indexes['xg'] = xg_id
            if gcsa_file_ids and gcsa_file_ids[i] is not None:
                indexes['gcsa'], indexes['lcp'] = gcsa_file_ids[i]
            if gbwt_file_ids and gbwt_file_ids[i] is not None:
                indexes['gbwt'] = gbwt_file_ids[i]
            if id_range_file_ids and id_range_file_ids[i] is not None:
                indexes['id_ranges'] = id_range_file_ids[i]
            if snarl_file_ids and snarl_file_ids[i] is not None:
                indexes['snarls'] = snarl_file_ids[i]
                
            # Put the indexes in the list of index dicts for each graph
            index_ids.append(indexes)

    
    return index_ids

def run_map_eval_align(job, context, index_ids, xg_comparison_ids, gam_names, gam_file_ids,
                       reads_fastq_single_ids, reads_fastq_paired_ids, reads_fastq_paired_for_vg_ids,
                       fasta_file_id, bwa_index_ids, matrix, ignore_quals, surject):
    """
    
    Run alignments, if alignment files have not already been provided.
    
    Returns a list of graph/gam names (with condition tags), a list of
    associated gam file IDs, a list of associated xg index IDs, and a list of
    BAM file IDs (or Nones) for realigned read BAMs, and a list of running
    times (for map commands not including toil-vg overhead)
    
    We need to modify the name and index lists because we synthesize paired-end
    versions of existing entries.
    
    Determines what conditions and combinations of conditions to run by looking
    at the "matrix" parameter, which is a dict from string variable name to a
    list of values for that variable. All sensible combinations of the variable
    values from the matrix are run as conditions.
    
    Variables to be used in the matrix are:
    
    "aligner": ["vg", "bwa"]
    
    "multipath": [True, False]
    
    "paired": [True, False]
    
    "gbwt": [False, True, <float log recombination penalty override>, ...]
   
    Additionally, mpmap_opts and more_mpmap_opts from the context's config are
    consulted, doubling the mpmap runs if more_mpmap_opts is set.
   
    If gam_file_ids are specified, passes those through instead of doing any vg
    mapping, but still does bwa mapping if requested.
    
    """

    # The input GAM names must be unique
    RealtimeLogger.info('Input GAM names: {}'.format(gam_names))
    assert(len(set(gam_names)) == len(gam_names))

    # scrape out the xg ids, don't need others any more after this step
    xg_ids = [index_id['xg'] for index_id in index_ids]

    # these indexes are passed out (not used for mapping), so we can
    # override them with our comparison indexes here
    if xg_comparison_ids:
        # optional override of downstream xg indexes via command line
        assert len(xg_comparison_ids) == len(xg_ids)

        # Count up how many xg IDs will actually be replaced
        overridden = 0
        for item in xg_comparison_ids:
            if item not in xg_ids:
                overridden += 1

        xg_ids = xg_comparison_ids

        # Stick the override xg into our index dictionary so it can be used for surjection
        for index_id, comparison_xg_id in zip(index_ids, xg_comparison_ids):
            index_id['xg-surject'] = comparison_xg_id
            
        RealtimeLogger.info('Applied {} xg overrides'.format(overridden))
    else:
        RealtimeLogger.info('No xg overrides applied')

    # the ids and names we pass forward
    out_xg_ids = xg_ids if gam_file_ids else []
    out_gam_names = gam_names if gam_file_ids else []

    # the map times
    map_times = [None] * len(gam_file_ids) if gam_file_ids else []

    # we use this hack to run multiple batches of mpmap opts
    mpmap_opts_list = [context.config.mpmap_opts]
    if context.config.more_mpmap_opts:
        mpmap_opts_list += context.config.more_mpmap_opts

    if ignore_quals:
        # Make sure we don't use quality adjusted alignment 
        for mpmap_opts in mpmap_opts_list:
            if '-A' not in mpmap_opts and '--no-qual-adjust' not in mpmap_opts:
                mpmap_opts.append('-A')
        context.config.map_opts = [o for o in context.config.map_opts if o not in ['-A', '--qual-adjust']]

    def fq_names(fq_reads_ids):
        return ['input{}.fq.gz'.format(i) for i in range(len(fq_reads_ids))]

    # Define some generators to expand conditions. Each takes a generator of
    # conditions to loop over, and yields those back again, possibly duplicated
    # and with more variables filled in.
    
    # This one expands all conditions by aligner
    def aligner_conditions(conditions_in):
        for condition in conditions_in:
            # Every condition gets expanded by aligner
            for aligner in matrix["aligner"]:
                extended = dict(condition)
                extended.update({"aligner": aligner})
                yield extended
    
    # This one expands vg conditions by whether to use mpmap or not
    def multipath_conditions(conditions_in):
        for condition in conditions_in:
            if condition["aligner"] == "vg":
                # Only vg conditions get expanded by multipath or not
                for multipath in matrix["multipath"]:
                    extended = dict(condition)
                    extended.update({"multipath": multipath})
                    yield extended
            else:
                yield condition
                
    # This one expands vg mpmap conditions by which mpmap option set should be
    # used (as an int index into mpmap_opts_list).
    # TODO: Make this come through the matrix and not a separate list
    def multipath_opts_conditions(conditions_in):
        for condition in conditions_in:
            if condition["aligner"] == "vg" and condition["multipath"] == True:
                # Only vg mpmap conditions get expanded by option set
                for opt_num in range(len(mpmap_opts_list)):
                    extended = dict(condition)
                    extended.update({"opt_num": opt_num})
                    yield extended
            else:
                yield condition
                
    # This one expands all conditions by whether to do paired-end or single-end
    # mapping
    def paired_conditions(conditions_in):
        for condition in conditions_in:
            for paired in matrix["paired"]:
                extended = dict(condition)
                extended.update({"paired": paired})
                yield extended
                
    # This one expands vg conditions by whether to use the gbwt index for
    # haplotype-aware mapping or not
    def gbwt_conditions(conditions_in):
        for condition in conditions_in:
            if condition["aligner"] == "vg":
                # Both vg map and vg mpmap conditions get expanded by gbwt or not
                for gbwt in matrix["gbwt"]:
                    extended = dict(condition)
                    extended.update({"gbwt": gbwt})
                    yield extended
            else:
                yield condition
                
    # We use this to compose all the generators together
    def compose_two_generators(gen1, gen2):
        def composed_generator(x):
            return gen2(gen1(x))
        return composed_generator
                
    # Define the list of functions to nest, innermost first. To add another
    # independent variable to the experiment, write another condition-expanding
    # generator function above and put it at the end of this list.
    condition_steps = [aligner_conditions, multipath_conditions, multipath_opts_conditions, paired_conditions, gbwt_conditions]
    # Make the master condition generator by composing all the generator
    # functions, left-inside-right. To use it, pass it a list of an empty dict
    # and loop over the fleshed-out condition dicts it generates.
    condition_generator = reduce(compose_two_generators, condition_steps)
    
    
    # Determine if we should do vg mapping or if we have gams already
    do_vg_mapping = not gam_file_ids
    # If we don't have them already, make an empty list.
    gam_file_ids = gam_file_ids or []
    
    # If bwa is not run, we need some Nones for its results
    bwa_bam_file_ids, bwa_mem_times = [None, None], [None, None]
    # And if it is run it will all run under this job, which starts out as None
    bwa_start_job = None

    # If --surject option used, keep track of the various surjection output in one dict
    surjected_results = {'bam_file_ids' : [],
                         'pe_bam_file_ids' : [],
                         'bam_names' : [],
                         'pe_bam_names' : [] }
    
    # Because we run multiple rounds of mapping the same reads, we want to
    # split the reads in advance. But we don't want to split reads in ways that
    # are unnecessary (e.g. single-end when we are only doing paired end). So
    # this dict maps from tuples of FASTQ IDs to the Toil job for splitting
    # those FASTQs with run_split_reads_if_needed.
    read_chunk_jobs = {}
    
    # Track the tag strings that are used. Each must be unique to ensure our GAM names are unique.
    used_tag_strings = set()
    
    
    RealtimeLogger.info('Condition matrix: {}'.format(matrix))
    
    for condition in condition_generator([{}]):
        # For each condition
        if condition["aligner"] == "vg" and do_vg_mapping:
            # This condition requires running vg and we aren't just using pre-run GAMs.
            
            # VG alignments get a tag string to distinguish the output GAMs.
            # It comes out something like "-mp-pe".
            tag_string = ""
           
            if condition["gbwt"]:
                # Mark as gbwt first if applicable
                
                if condition["gbwt"] == True:
                    # We just use the default value (no number)
                    tag_string += "-gbwt"
                else:
                    # It must be a number
                    tag_string += "-gbwt{}".format(condition["gbwt"])
           
            if condition["multipath"]:
                # Doing multipath mapping
                tag_string += "-mp"
                tag_string += (str(condition["opt_num"]) if condition["opt_num"] > 0 else '')
                
                # Prepare a context for multipath mapping with the appropriate option set.
                mapping_context = copy.deepcopy(context)
                mapping_context.config.mpmap_opts = mpmap_opts_list[condition["opt_num"]]
            else:
                # Just use the normal context we have
                mapping_context = context
            
            if condition["paired"]:
                # Add the paired end tag
                tag_string += "-pe"
                # Make sure we have paired data
                assert reads_fastq_paired_for_vg_ids
                fastq_ids = reads_fastq_paired_for_vg_ids
                # And determine if it is interleaved...
                interleaved = len(reads_fastq_paired_for_vg_ids) == 1
                if not interleaved:
                    # ...or if we know we are paired by having 2 files.
                    assert len(reads_fastq_paired_for_vg_ids) == 2
            else:
                # Make sure we have single-end data
                assert reads_fastq_single_ids
                # And that it won't be seen as paired non-interleaved
                assert len(reads_fastq_single_ids) == 1
                fastq_ids = reads_fastq_single_ids
                # It is never interleaved
                interleaved = False
                
            # Now the tag string is complete
            RealtimeLogger.info('Condition {} produced tag string {}'.format(condition, tag_string))
            if tag_string in used_tag_strings:
                # If it's a duplicate, bail out
                raise RuntimeError('Duplicate tag string {}'.format(tag_string))
            else:
                # Otherwise, say we used it
                used_tag_strings.add(tag_string)
                
            # If we have a GBWT penalty override, what is it?
            gbwt_penalty = None
            if condition["gbwt"] and condition["gbwt"] != True:
                gbwt_penalty = condition["gbwt"]
                
            # We collect all the map jobs in a list for each index, so we can update all our output lists for them
            map_jobs = []
                    
            for i, indexes in enumerate(index_ids):
                # Map or mpmap, paired or not as appropriate, against each index set.
                
                if not condition["gbwt"]:
                    # Drop the GBWT index if present for the non-GBWT conditions
                    # TODO: we know things don't have GBWTs because their GBWT and no-GBWT results are the same...
                    indexes = dict(indexes)
                    if indexes.has_key("gbwt"):
                        del indexes["gbwt"]
                        
                if not read_chunk_jobs.has_key(tuple(fastq_ids)):
                    # We have not yet asked to split the appropriate FASTQs.
                    # Make a job to do that, and save it so we can grab its rv later.
                    read_chunk_jobs[tuple(fastq_ids)] = job.addChildJobFn(run_split_reads_if_needed, context, fq_names(fastq_ids),
                                                                          None, None, fastq_ids,
                                                                          cores=context.config.misc_cores,
                                                                          memory=context.config.misc_mem,
                                                                          disk=context.config.misc_disk)
                    
                # Find the appropriate read chunking job that the mapping needs to come after.
                read_chunk_job = read_chunk_jobs[tuple(fastq_ids)]
                
                # After the reads we need are split into chunks, map them.
                map_jobs.append(read_chunk_job.addFollowOnJobFn(run_mapping, mapping_context, fq_names(fastq_ids),
                                                                None, None, 'aligned-{}{}'.format(gam_names[i], tag_string),
                                                                interleaved, condition["multipath"], indexes,
                                                                reads_chunk_ids=read_chunk_job.rv(),
                                                                bam_output=False, surject=surject,
                                                                gbwt_penalty=gbwt_penalty,
                                                                cores=mapping_context.config.misc_cores,
                                                                memory=mapping_context.config.misc_mem,
                                                                disk=mapping_context.config.misc_disk))
                                    
            for i, map_job in enumerate(map_jobs):
                # Update our output lists for every mapping job we are running
                gam_file_ids.append(map_job.rv(0))
                map_times.append(map_job.rv(1))
                out_xg_ids.append(xg_ids[i])
                out_gam_names.append(gam_names[i] + tag_string)
                if condition['paired']:
                    surjected_results['pe_bam_file_ids'].append(map_job.rv(2))
                    surjected_results['pe_bam_names'].append(out_gam_names[-1] + '-surject')
                else:
                    surjected_results['bam_file_ids'].append(map_job.rv(2))
                    surjected_results['bam_names'].append(out_gam_names[-1] + '-surject')
            
        elif condition["aligner"] == "bwa":
            # Run BWA.
            if bwa_start_job is None:
                # If we do any BWA we need this job to exist
                bwa_start_job = Job()
                job.addChild(bwa_start_job)
                bwa_index_job = bwa_start_job.addChildJobFn(run_bwa_index, context,
                                                            fasta_file_id,
                                                            bwa_index_ids=bwa_index_ids,
                                                            intermediate=True,
                                                            cores=context.config.bwa_index_cores, memory=context.config.bwa_index_mem,
                                                            disk=context.config.bwa_index_disk)
                bwa_index_ids = bwa_index_job.rv()
                    
            if condition["paired"]:
                # Do paired-end BWA
                assert reads_fastq_paired_ids
                bwa_mem_job = bwa_start_job.addFollowOnJobFn(run_bwa_mem, context, reads_fastq_paired_ids, bwa_index_ids, True,
                                                             cores=context.config.alignment_cores, memory=context.config.alignment_mem,
                                                             disk=context.config.alignment_disk)
                bwa_bam_file_ids[1] = bwa_mem_job.rv(0)
                bwa_mem_times[1] = bwa_mem_job.rv(1)
            else:
                # Do single-ended
                assert reads_fastq_single_ids
                bwa_mem_job = bwa_start_job.addFollowOnJobFn(run_bwa_mem, context, reads_fastq_single_ids, bwa_index_ids, False,
                                                             cores=context.config.alignment_cores, memory=context.config.alignment_mem,
                                                             disk=context.config.alignment_disk)
                bwa_bam_file_ids[0] = bwa_mem_job.rv(0)
                bwa_mem_times[0] = bwa_mem_job.rv(1)

    # GAM names must be unique
    RealtimeLogger.info('Output GAM names: {}'.format(out_gam_names))
    assert(len(set(out_gam_names)) == len(out_gam_names))

    return (out_gam_names, gam_file_ids, out_xg_ids, map_times, bwa_bam_file_ids,
            bwa_mem_times, surjected_results)
    
def run_map_eval_comparison(job, context, xg_file_ids, gam_names, gam_file_ids,
                            bam_names, bam_file_ids, pe_bam_names, pe_bam_file_ids,
                            bwa_bam_file_ids, surjected_results, true_read_stats_file_id,
                            mapeval_threshold, score_baseline_name=None, original_read_gam=None,
                            downsample_portion=None, gbwt_usage_tag_gam_name=None):
    """
    run the mapping comparison.  Dump some tables into the outstore.
    
    Returns a pair of the position comparison results and the score comparison
    results.
    
    The score comparison results are a dict from baseline name to comparison
    against that baseline. Each comparison's data is a tuple of a list of
    individual per-graph comparison file IDs and an overall stats file for that
    comparison.
    
    If score_baseline_name is specified, all GAMs have their scores compared
    against the scores from the GAM with that name as a baseline.
    
    If original_read_gam is specified, all GAMs have their scores compared
    against that GAM's scores as a baseline.
    
    Each result set is itself a pair, consisting of a list of per-graph file
    IDs, and an overall statistics file ID.
    
    If downsample_portion is specified, the comparison runs on a downsampled
    porton of the reads.
    
    If gbwt_usage_tag_gam_name is set, tags for that GAM's reads' GBWT usage
    annotations will be generated for the GAM with that name, and propagated to
    all the other conditions nin the combined stats file.
    
    """
    
    # munge out the returned pair of BAMs
    if bwa_bam_file_ids[0] is not None:
        bam_file_ids.append(bwa_bam_file_ids[0])
        bam_names.append('bwa-mem')
    if bwa_bam_file_ids[1] is not None:
        pe_bam_file_ids.append(bwa_bam_file_ids[1])
        pe_bam_names.append('bwa-mem-pe')

    # and also in the surjected BAMs to the lists we're passing along to comparison
    for bam_name, surjected_bam_file_id in zip(surjected_results['bam_names'],
                                               surjected_results['bam_file_ids']):
        if surjected_bam_file_id:
            if type(surjected_bam_file_id) is list:
                assert len(surjected_bam_file_id) == 1
                bam_file_ids.append(surjected_bam_file_id[0])
            else:
                bam_file_ids.append(surjected_bam_file_id)
            bam_names.append(bam_name)
    for pe_bam_name, surjected_pe_bam_file_id in zip(surjected_results['pe_bam_names'],
                                                     surjected_results['pe_bam_file_ids']):
        if surjected_pe_bam_file_id:
            if type(surjected_pe_bam_file_id) is list:
                assert len(surjected_pe_bam_file_id) == 1
                pe_bam_file_ids.append(surjected_pe_bam_file_id[0])
            else:
                pe_bam_file_ids.append(surjected_pe_bam_file_id)
            pe_bam_names.append(pe_bam_name)
        
    # We need to keep the BAM stats jobs around to wait on them
    bam_stats_jobs = []

    # get the bwa read alignment statistics, one id for each bam_name
    bam_stats_file_ids = []
    for bam_i, bam_id in enumerate(bam_file_ids):
        
        # What job ensures we have the alignments to evaluate?
        parent_job = job
        if downsample_portion is not None and downsample_portion != 1.0:
            # Downsample the BAM
            parent_job = job.addChildJobFn(downsample_bam, context, bam_id, downsample_portion,
                                           cores=context.config.misc_cores, memory=context.config.misc_mem,
                                           disk=bam_id.size * 2)
            bam_id = parent_job.rv()
    
        name = '{}-{}.bam'.format(bam_names[bam_i], bam_i)
        bam_stats_jobs.append(parent_job.addChildJobFn(extract_bam_read_stats, context, name, bam_id, False,
                                                       cores=context.config.misc_cores, memory=context.config.misc_mem,
                                                       disk=context.config.alignment_disk))
        bam_stats_file_ids.append(bam_stats_jobs[-1].rv())
    # separate flow for paired end bams because different logic used
    pe_bam_stats_file_ids = []
    for bam_i, bam_id in enumerate(pe_bam_file_ids):
        
        # What job ensures we have the alignments to evaluate?
        parent_job = job
        if downsample_portion is not None and downsample_portion != 1.0:
            # Downsample the BAM
            parent_job = job.addChildJobFn(downsample_bam, context, bam_id, downsample_portion,
                                           cores=context.config.misc_cores, memory=context.config.misc_mem,
                                           disk=bam_id.size * 2)
            bam_id = parent_job.rv()
    
        name = '{}-{}.bam'.format(pe_bam_names[bam_i], bam_i)
        bam_stats_jobs.append(parent_job.addChildJobFn(extract_bam_read_stats, context, name, bam_id, True,
                                                       cores=context.config.misc_cores, memory=context.config.misc_mem,
                                                       disk=context.config.alignment_disk))
        pe_bam_stats_file_ids.append(bam_stats_jobs[-1].rv())

    # get the gam read alignment statistics, one for each gam_name (todo: run vg map like we do bwa?)
    gam_stats_file_ids = []
    # We also need to keep the jobs around so we can enforce that things run after them.
    gam_stats_jobs = []
    for gam_i, gam_id in enumerate(gam_file_ids):
        name = '{}-{}.gam'.format(gam_names[gam_i], gam_i)
        # run_mapping will return a list of gam_ids.  since we don't
        # specify id ranges, this will always have one entry
        gam = gam_id
        if type(gam_id) is list:
            assert len(gam_id) == 1
            gam = gam_id[0]
        RealtimeLogger.info('Work on GAM {} = {} named {} with XG id {}'.format(gam_i, gam, gam_names[gam_i], xg_file_ids[gam_i]))
        
        # What job ensures we have the alignments to evaluate?
        parent_job = job
        if downsample_portion is not None and downsample_portion != 1.0:
            # Downsample the GAM
            parent_job = job.addChildJobFn(downsample_gam, context, gam, downsample_portion,
                                           cores=context.config.misc_cores, memory=context.config.misc_mem,
                                           disk=gam.size * 2)
            gam = parent_job.rv()
        
        # Make a job to annotate the GAM
        annotate_job = parent_job.addChildJobFn(annotate_gam, context, xg_file_ids[gam_i], gam,
                                                cores=context.config.misc_cores, memory=context.config.alignment_mem,
                                                disk=context.config.alignment_disk)
        
        # Determine the annotations to promote to tags
        generate_tags = []
        if gam_names[gam_i] == gbwt_usage_tag_gam_name:
            # We need to produce tags for the haplotype-scored-ness annotation
            # for this GAM condition so we can propagate them later.
            generate_tags.append('haplotype_score_used')
        
        # Then compute stats on the annotated GAM
        gam_stats_jobs.append(annotate_job.addFollowOnJobFn(extract_gam_read_stats, context,
                                                            name, annotate_job.rv(),
                                                            generate_tags=generate_tags,
                                                            cores=context.config.misc_cores, memory=context.config.misc_mem,
                                                            disk=context.config.alignment_disk))
        
        gam_stats_file_ids.append(gam_stats_jobs[-1].rv())

    # compare all our positions, and dump results to the out store. Get a tuple
    # of individual comparison files and overall stats file.
    position_comparison_job = job.addChildJobFn(run_map_eval_compare_positions, context,
                                                true_read_stats_file_id, gam_names, gam_stats_file_ids,
                                                bam_names, bam_stats_file_ids, pe_bam_names, pe_bam_stats_file_ids,
                                                mapeval_threshold, gbwt_usage_tag_gam_name=gbwt_usage_tag_gam_name,
                                                cores=context.config.misc_cores, memory=context.config.misc_mem,
                                                disk=context.config.misc_disk)
    for dependency in itertools.chain(gam_stats_jobs, bam_stats_jobs):
        dependency.addFollowOn(position_comparison_job)
    position_comparison_results = position_comparison_job.rv()
    
    # This will map from baseline name to score comparison data against that
    # baseline
    score_comparisons = {}
    
    if score_baseline_name is not None:
        # We want to compare the scores from all the GAMs against a baseline
        
        # Make a dict mapping from assigned GAM name in gam_names to the stats file for that GAM's alignment
        name_to_stats_id = dict(itertools.izip(gam_names, gam_stats_file_ids))
        
        # Find the baseline scores
        baseline_stats_id = name_to_stats_id[score_baseline_name]
        
        # compare all our scores against the baseline, and dump results to the
        # out store. 
        score_comp_job = job.addChildJobFn(run_map_eval_compare_scores, context, score_baseline_name, baseline_stats_id,
                                           gam_names, gam_stats_file_ids, bam_names, bam_stats_file_ids,
                                           pe_bam_names, pe_bam_stats_file_ids, cores=context.config.misc_cores,
                                           memory=context.config.misc_mem, disk=context.config.misc_disk)
        for dependency in itertools.chain(gam_stats_jobs, bam_stats_jobs):
            dependency.addFollowOn(score_comp_job)
                             
        # Get a tuple of individual comparison files and overall stats file.
        score_comparisons[score_baseline_name] = score_comp_job.rv()
        
    if original_read_gam is not None:
        # Also compare against the original GAM's scores as a baseline
        
        # First compute its stats file
        stats_job = job.addChildJobFn(extract_gam_read_stats, context,
                                      name, original_read_gam,
                                      cores=context.config.misc_cores, memory=context.config.misc_mem,
                                      disk=context.config.alignment_disk)
        
        # compare all our scores against this other baseline, and dump results
        # to the out store.
        score_comp_job = stats_job.addFollowOnJobFn(run_map_eval_compare_scores, context, 'input', stats_job.rv(),
                                                    gam_names, gam_stats_file_ids, bam_names, bam_stats_file_ids,
                                                    pe_bam_names, pe_bam_stats_file_ids, cores=context.config.misc_cores,
                                                    memory=context.config.misc_mem, disk=context.config.misc_disk)
                                                    
        for dependency in itertools.chain(gam_stats_jobs, bam_stats_jobs):
            dependency.addFollowOn(score_comp_job)
                                                    
        # Save the results
        score_comparisons['input'] = score_comp_job.rv()
        
        
        
    return position_comparison_results, score_comparisons

def run_map_eval_compare_positions(job, context, true_read_stats_file_id, gam_names, gam_stats_file_ids,
                         bam_names, bam_stats_file_ids, pe_bam_names, pe_bam_stats_file_ids, mapeval_threshold,
                         gbwt_usage_tag_gam_name=None):
    """
    Compare the read positions for each read across the different aligmment
    methods.
    
    Produces a bunch of individual comparison files against the truth (in TSV
    format), a combined "positions.results.tsv" across all aligners, and a
    statistics file "stats.tsv" in the out_store.
    
    If gbwt_usage_tag_gam_name is set, propagates the GBWT usage tag from the
    stats file for that GAM to the stats files for all the other conditions.
    
    Returns the list of comparison files, and the stats file ID.
    """

    # merge up all the output data into one list
    names = gam_names + bam_names + pe_bam_names
    stats_file_ids = gam_stats_file_ids + bam_stats_file_ids + pe_bam_stats_file_ids
    
    # Make sure each name appears only once overall
    assert(len(set(names)) == len(names))
    
    # This is the job that roots the position comparison
    root = job
    
    if gbwt_usage_tag_gam_name is not None:
        # We want to propagate the GBWT usage tag from this GAM's stats file. Find it.
        tag_gam_index = gam_names.index(gbwt_usage_tag_gam_name)
        tag_stats_id = gam_stats_file_ids[tag_gam_index]
        
        # This holds the IDs of the stats files that have had the tags propagated.
        propagated_stats_file_ids = []
        for other_id in stats_file_ids:
            propagate_job = job.addChildJobFn(propagate_tag, context, tag_stats_id, other_id, 'haplotype_score_used',
                                              cores=context.config.misc_cores, memory=context.config.misc_mem,
                                              disk=context.config.alignment_disk)
            propagated_stats_file_ids.append(propagate_job.rv())
        
        # Mak a new root for the position comparison after that.
        root = Job()
        job.addFollowOn(root)
        
        # Use the improved stats files instead fo the old ones
        stats_file_ids = propagated_stats_file_ids
        
        

    compare_ids = []
    for name, stats_file_id in zip(names, stats_file_ids):
        # When the (modified) individual stats files are ready, run the position comparison
        compare_ids.append(root.addChildJobFn(compare_positions, context, true_read_stats_file_id, name,
                                              stats_file_id, mapeval_threshold,
                                              cores=context.config.misc_cores, memory=context.config.misc_mem,
                                              disk=context.config.alignment_disk).rv())

    position_comp_file_id = root.addFollowOnJobFn(run_process_position_comparisons, context, names, compare_ids,
                                                  cores=context.config.misc_cores, memory=context.config.misc_mem,
                                                  disk=context.config.alignment_disk).rv(1)
                                         
    return compare_ids, position_comp_file_id
    
def propagate_tag(job, context, from_id, to_id, tag_name):
    """
    Given two positiuon stats TSVs, of the format:
    
    read name, read tags (or '.'), [contig aligned to, alignment position,]* score, MAPQ
    
    Copies the tag of the given name, if present, from the from file to the to file for corresponding reads.
    
    Works even if files are not sorted by read name.
    
    Returns the ID of the modified to file.
    
    """
    
    if from_id == to_id:
        # Nothing to do! All tags will be the same.
        return to_id
    
    work_dir = job.fileStore.getLocalTempDir()
    
    from_stats_file = os.path.join(work_dir, 'from.tsv')
    job.fileStore.readGlobalFile(from_id, from_stats_file, cache=False)
    to_stats_file = os.path.join(work_dir, 'to.tsv')
    job.fileStore.readGlobalFile(to_id, to_stats_file, cache=False)

    # Sort the input files in place
    cmd = ['sort', os.path.basename(from_stats_file), '-k', '1', '-o', os.path.basename(from_stats_file)]
    context.runner.call(job, cmd, work_dir = work_dir)
    cmd = ['sort', os.path.basename(to_stats_file), '-k', '1', '-o', os.path.basename(to_stats_file)]
    context.runner.call(job, cmd, work_dir = work_dir)
    
    
    with open(from_stats_file) as from_stream, \
        open(to_stats_file) as to_stream, \
        job.fileStore.writeGlobalFileStream() as (out_stream, out_id):
        
        # Read the file we are pulling the tag from
        from_reader = iter(tsv.TsvReader(from_stream))
        
        # And the file we are putting the tag to
        to_reader = iter(tsv.TsvReader(to_stream))
        
        # And set up the output writer
        out_writer = tsv.TsvWriter(out_stream)
        
        # Start an iteration over them
        from_fields = next(from_reader, None)
        to_fields = next(to_reader, None)
        
        # Track line numbers for error reporting
        from_line = 1
        to_line = 1
        
        try:
        
            while from_fields is not None and to_fields is not None:
                # We still have data on both sides
                
                # The minimum field count you can have for either side is 4
                
                if len(from_fields) < 4:
                    raise RuntimeError('Incorrect (<6) source field count on line {}: {}'.format(
                        from_line, from_fields))
                
                if len(to_fields) < 4:
                    raise RuntimeError('Incorrect (<4) destination field count on line {}: {}'.format(
                        to_line, to_fields))
                
                from_read_name = from_fields[0]
                to_read_name = to_fields[0]
                
                if from_read_name != to_read_name:
                    # The reads should correspond; any downsampling should have already happened.
                    # If not, report something hopefully informative.
                    raise RuntimeError('Name {} on line {} does not match {} on line {}'.format(
                        from_read_name, from_line, to_read_name, to_line))
                    
                # Parse the comma-separated tags from the from file.
                from_tags = from_fields[1]
                if from_tags in ['', '.']:
                    from_tags = set()
                else:
                    from_tags = set(from_tags.split(','))
                
                # And from the to file
                to_tags = to_fields[1]
                if to_tags in ['', '.']:
                    to_tags = set()
                else:
                    to_tags = set(to_tags.split(','))
                    
                
                if tag_name in from_tags and tag_name not in to_tags:
                    # This tag needs to be added in
                    to_tags.add(tag_name)
                elif tag_name not in from_tags and tag_name in to_tags:
                    # The tag is there when it shouldn't be and needs to be removed
                    to_tags.remove(tag_name)
                    
                
                # Convert back to a comma-separated string or .
                if len(to_tags) == 0:
                    to_tags = '.'
                else:
                    to_tags = ','.join(to_tags)
                    
                to_fields[1] = to_tags

                out_writer.list_line(to_fields)
        
                # Advance both reads
                from_fields = next(from_reader, None)
                from_line += 1
                to_fields = next(to_reader, None)
                to_line += 1
                
        except:
            
            logging.error("Tag propagation failed. Dumping files.")
            context.write_output_file(job, from_stats_file)
            context.write_output_file(job, to_stats_file)
            
            raise
            
    # Return the ID of the file we wrote.
    return out_id
    

def run_process_position_comparisons(job, context, names, compare_ids):
    """
    Write some raw tables of position comparisons to the output.  Compute some
    stats for each graph.

    The position results file format is a TSV of:
    correct flag, mapping quality, tag list (or '.'), method name, read name (or '.'), weight (or 1)

    
    Returns (the stats file's file ID, the position results file's ID)
    """

    work_dir = job.fileStore.getLocalTempDir()

    map_stats = []
    
    RealtimeLogger.info("Processing position comparisons for conditions: {}".format(names))
    
    # Only allow each condition to appear once.
    # If this is violated, something has gone wrong in our naming.
    assert(len(set(names)) == len(names))

    # make the position.results.tsv and position.stats.tsv
    results_file = os.path.join(work_dir, 'position.results.tsv')
    with open(results_file, 'w') as out_stream:
        out_results = tsv.TsvWriter(out_stream)
        # Put a header
        out_results.list_line(['correct', 'mq', 'tags', 'aligner', 'read', 'count'])

        def write_tsv(comp_file, method):
            """
            Read the given comparison TSV for the given condition name, and dump
            it to the combined results file.
            """
            
            # The vg R scripts are responsible for determining a smart method name sort order now.
           
            with open(comp_file) as comp_in_stream:
                comp_in = tsv.TsvReader(comp_in_stream)
                # This will hold counts for (correct, mq, tags, method) tuples.
                # Tags are represented as a string.
                # We only summarize correct reads.
                summary_counts = Counter()
                # Wrong reads are just dumped as they occur with count 1
                for toks in comp_in:
                    # Label the read fields so we can see what we're doing
                    # Note that empty 'tags' columns may not be read by the TSV reader.
                    read = dict(zip(['name', 'correct', 'mapq', 'tags'], toks))
                    
                    if read['correct'] == '1':
                        # Correct, so summarize
                        summary_counts[(read['correct'], read['mapq'], read.get('tags', '.'), method)] += 1
                    else:
                        # Incorrect, write the whole line
                        out_results.line(read['correct'], read['mapq'], read.get('tags', '.'), method, read['name'], 1)
                for parts, count in summary_counts.iteritems():
                    # Write summary lines with empty read names
                    # Omitting the read name entirely upsets R, so we will use a dot as in VCF for missing data.
                    out_results.list_line(list(parts) + ['.', count])

        for name, compare_id in itertools.izip(names, compare_ids):
            compare_file = os.path.join(work_dir, '{}.compare.positions'.format(name))
            job.fileStore.readGlobalFile(compare_id, compare_file)
            context.write_output_file(job, compare_file)
            write_tsv(compare_file, name)

            map_stats.append([job.addChildJobFn(run_acc, context, name, compare_id, cores=context.config.misc_cores,
                                                memory=context.config.misc_mem, disk=context.config.misc_disk).rv(),
                              job.addChildJobFn(run_auc, context, name, compare_id, cores=context.config.misc_cores,
                                                memory=context.config.misc_mem, disk=context.config.misc_disk).rv(),
                              job.addChildJobFn(run_qq, context, name, compare_id, cores=context.config.misc_cores,
                                                memory=context.config.misc_mem, disk=context.config.misc_disk).rv(),
                              job.addChildJobFn(run_max_f1, context, name, compare_id, cores=context.config.misc_cores,
                                                memory=context.config.misc_mem, disk=context.config.misc_disk).rv()])
            
    position_results_id = context.write_output_file(job, results_file)

    return job.addFollowOnJobFn(run_write_position_stats, context, names, map_stats).rv(), position_results_id

def run_write_position_stats(job, context, names, map_stats):
    """
    write the position comparison statistics as tsv, both to the Toil fileStore
    and to the out_store as "stats.tsv".
    
    Returns the ID of the file written.
    
    This is different than the stats TSV format used internally, for read stats.
    """

    work_dir = job.fileStore.getLocalTempDir()
    stats_file = os.path.join(work_dir, 'stats.tsv')
    with open(stats_file, 'w') as stats_out:
        stats_out.write('aligner\tcount\tacc\tauc\tqq-r\tmax-f1\n')
        for name, stats in zip(names, map_stats):
            stats_out.write('{}\t{}\t{}\t{}\t{}\t{}\n'.format(name, stats[0][0], stats[0][1],
                                                          stats[1][0], stats[2], stats[3]))

    stats_file_id = context.write_output_file(job, stats_file)
    
    return stats_file_id
    
def run_acc(job, context, name, compare_id):
    """
    Percentage of correctly aligned reads (ignore quality)

    Comparison file input must be TSV with one row per read, column 0 unused
    and column 1 as the correct flag.
    """
    
    work_dir = job.fileStore.getLocalTempDir()

    compare_file = os.path.join(work_dir, '{}.compare.positions'.format(name))
    job.fileStore.readGlobalFile(compare_id, compare_file)
    
    total = 0
    correct = 0
    with open(compare_file) as compare_f:
        for toks in tsv.TsvReader(compare_f):
            total += 1
            if toks[1] == '1':
                correct += 1
                
    acc = float(correct) / float(total) if total > 0 else 0
    return total, acc
    
def run_auc(job, context, name, compare_id):
    """
    AUC of roc plot.
    
    ROC plot is defined with mismapped reads being negatives, correctly-mapped
    reads being positives, and AUC expressing how good of a classifier of
    correctly-mapped-ness the MAPQ score is. It says nothing about how well the
    reads are actually mapped.

    Comparison file input must be TSV with one row per read, column 0 unused,
    column 1 as the correct flag, and column 2 as the MAPQ.
    
    """
    if not have_sklearn:
        return ["sklearn_not_installed"] * 2 
    
    work_dir = job.fileStore.getLocalTempDir()

    compare_file = os.path.join(work_dir, '{}.compare.positions'.format(name))
    job.fileStore.readGlobalFile(compare_id, compare_file)

    try:
        data = np.loadtxt(compare_file, dtype=np.int, delimiter ='\t', usecols=(1,2)).T
        auc = roc_auc_score(data[0], data[1])
        aupr = average_precision_score(data[0], data[1])
    except:
        # will happen if file is empty
        auc, aupr = 0, 0

    return auc, aupr
    
def run_max_f1(job, context, name, compare_id):
    """
    Compute and return maximum F1 score for correctly mapping reads, using MAPQ as a confidence.
    
    The problem is that read mapping is a multi-class classification problem with ~ 1 class per genome base, and F1 is a 2-class classification statistic. So we squish the concept a bit.
    
    For a given MAPQ threshold, we define a fake confusion matrix:
    
    TP = reads meeting threshold mapped correctly
    FP = reads meeting threshold mapped incorrectly
    TN = reads that didn't come from the target graph and didn't meet the threshold (i.e. 0 reads)
    FN = reads that weren't both correctly mapped and assigned a MAPQ meeting the threshold
    
    Then we calculate precision = TP / (TP + FP) and recall = TP / (TP + FN), and from those calculate an F1.
    Then we calculate the best F1 across all the MAPQ values.

    Comparison file input must be TSV with one row per read, column 0 unused,
    column 1 as the correct flag, and column 2 as the MAPQ.
    
    """
    if not have_sklearn:
        return "sklearn_not_installed" 
    
    work_dir = job.fileStore.getLocalTempDir()

    compare_file = os.path.join(work_dir, '{}.compare.positions'.format(name))
    job.fileStore.readGlobalFile(compare_id, compare_file)

    # Load up the correct/incorrect flag (data[_, 1]) and the scores (data[_, 2])
    data = np.loadtxt(compare_file, dtype=np.int, delimiter ='\t', usecols=(1,2))
    
    # Sort on score (see <https://stackoverflow.com/a/2828121/402891>) in
    # descending order. So reads we want to take first come first.
    data = data[data[:,1].argsort()[::-1]]
    
    # What's the last MAPQ we did?
    last_mapq = None
    
    # What so far is our confusion matrix?
    tp = 0
    fp = 0
    tn = 0
    fn = len(data)
    
    # What's our max f1?
    max_f1 = 0
    
    # And how do we calculate it?
    def emit_f1():
        if tp > 0 or (fp > 0 and fn > 0):
            # Safe to compute precision and recall, so do that.
            precision = float(tp) / (tp + fp)
            recall = float(tp) / (tp + fn)
            if precision > 0 or recall > 0:
                # Safe to compute an F1, so do that
                f1 = 2 * (precision * recall) / (precision + recall)
                return max(max_f1, f1)
        return max_f1
    
    for correct, score in data:
        # For each read in descending MAPQ order
        
        if score != last_mapq:
            # We're moving on to a new tranche
            max_f1 = emit_f1()
            
        # This read is now a positive. It may be true or false.
        if correct:
            tp += 1
        else:
            fp += 1
        # It is no longer a false negative
        fn -= 1
        
    # At the end of all the reads, that's another tranche done
    max_f1 = emit_f1()
        
    return max_f1

def run_qq(job, context, name, compare_id):
    """
    some measure of qq consistency

    Comparison file input must be TSV with one row per read, column 0 unused,
    column 1 as the correct flag, and column 2 as the MAPQ.
    """
    if not have_sklearn:
        return "sklearn_not_installed"

    work_dir = job.fileStore.getLocalTempDir()

    compare_file = os.path.join(work_dir, '{}.compare.positions'.format(name))
    job.fileStore.readGlobalFile(compare_id, compare_file)

    try:
        data = np.loadtxt(compare_file, dtype=np.int, delimiter ='\t', usecols=(1,2))

        # this can surley be sped up if necessary
        correct = Counter()
        total = Counter()
        for row in data:
            correct[row[1]] += row[0]
            total[row[1]] += 1

        qual_scores = []
        qual_observed = []            
        for qual, cor in correct.items():
            qual_scores.append(qual)
            p_err = max(1. - float(cor) / float(total[qual]), sys.float_info.epsilon)
            observed_score =-10. * math.log10(p_err)
            qual_observed.append(observed_score)

        # should do non-linear regression as well? 
        r2 = r2_score(qual_observed, qual_scores)
    except:
        # will happen if file is empty
        r2 = 'fail'

    return r2
    
def run_map_eval_compare_scores(job, context, baseline_name, baseline_stats_file_id, gam_names, gam_stats_file_ids,
                                bam_names, bam_stats_file_ids, pe_bam_names, pe_bam_stats_file_ids):
    """
    Compare scores in the given stats files in the lists to those in the given
    baseline stats file.
    
    Stats file format is a TSV of:
    read name, contig name, contig offset, score, mapping quality
    
    Will save the output to the outstore, as a CSV of read name and score
    difference, named <GAM/BAM name>.compare.<baseline name>.scores.
    
    Will also save a concatenated TSV file, with score difference and quoted
    aligner/condition name, as score.results.<baseline_name>.tsv
    
    Returns the list of comparison file IDs and the score results file ID.
    
    For now, just ignores BAMs because we don't pull in pysam to parse out their
    scores.
    
    """
    
    # merge up all the condition names and file IDs into synchronized lists
    # TODO: until we can extract the scores from BAMs, just process the GAMs
    names = gam_names
    stats_file_ids = gam_stats_file_ids
    
    RealtimeLogger.info(names)
    RealtimeLogger.info(stats_file_ids)

    compare_ids = []
    for name, stats_file_id in zip(names, stats_file_ids):
        compare_ids.append(job.addChildJobFn(compare_scores, context, baseline_name, baseline_stats_file_id, name, stats_file_id,
                                             cores=context.config.misc_cores, memory=context.config.misc_mem,
                                             disk=context.config.misc_disk).rv())

    stats_job = job.addFollowOnJobFn(run_process_score_comparisons, context, baseline_name, names, compare_ids,
                                     cores=context.config.misc_cores, memory=context.config.misc_mem,
                                     disk=context.config.misc_disk)
                                     
    return compare_ids, stats_job.rv()

def run_process_score_comparisons(job, context, baseline_name, names, compare_ids):
    """
    Write some raw tables of score comparisons against the given baseline to the
    output.  Compute some stats for each graph.
    
    Returns the file ID of the overall stats file "score.stats.<baseline name>.tsv".
    """

    work_dir = job.fileStore.getLocalTempDir()

    # Holds a list (by aligner) of lists (by type of statistic) of stats info
    # (that might be tuples, depending on the stat)
    # TODO: Change this to dicts by stat type.
    map_stats = []

    # make the score.results.tsv, which holds score differences and aligner/condition names.
    results_file = os.path.join(work_dir, 'score.{}.results.tsv'.format(baseline_name))
    with open(results_file, 'w') as out_results_file:
        out_results = tsv.TsvWriter(out_results_file)
        out_results.comment('diff\taligner')

        def write_tsv(comp_file, a):
            """
            Read the given comparison TSV for the given condition name, and dump
            it to the combined results file.
            """
            with open(comp_file) as comp_in:
                for line in comp_in:
                    content = line.rstrip()
                    if content != '':
                        toks = content.split(', ')
                        if len(toks) < 2:
                            raise RuntimeError('Invalid comparison file line ' + content)
                        out_results.line(toks[1], a)

        for name, compare_id in itertools.izip(names, compare_ids):
            compare_file = os.path.join(work_dir, '{}.compare.{}.scores'.format(name, baseline_name))
            job.fileStore.readGlobalFile(compare_id, compare_file)
            context.write_output_file(job, compare_file)
            write_tsv(compare_file, name)

            # Tabulate overall statistics
            map_stats.append([job.addChildJobFn(run_portion_worse, context, name, compare_id,
                                                cores=context.config.misc_cores, memory=context.config.misc_mem,
                                                disk=context.config.misc_disk).rv()])
            
    context.write_output_file(job, results_file)
    
    return job.addFollowOnJobFn(run_write_score_stats, context, baseline_name, names, map_stats).rv()
    
def run_write_score_stats(job, context, baseline_name, names, map_stats):
    """
    write the score comparison statistics against the baseline with the given
    name as tsv named "score.stats.<baseline name>.tsv".
    
    Returns the file ID for that file.
    
    This is different than the stats TSV format used internally, for read stats.
    """

    work_dir = job.fileStore.getLocalTempDir()
    stats_file = os.path.join(work_dir, 'score.stats.{}.tsv'.format(baseline_name))
    with open(stats_file, 'w') as stats_out_file:
        # Put each stat as a different column.
        stats_out = tsv.TsvWriter(stats_out_file)
        stats_out.comment('aligner\tcount\tworse')
        for name, stats in zip(names, map_stats):
            stats_out.line(name, stats[0][0], stats[0][1])

    return context.write_output_file(job, stats_file)
    
def run_portion_worse(job, context, name, compare_id):
    """
    Compute percentage of reads that get worse from the baseline graph.
    Return total reads and portion that got worse.
    """
    
    work_dir = job.fileStore.getLocalTempDir()

    compare_file = os.path.join(work_dir, '{}.compare.scores'.format(name))
    job.fileStore.readGlobalFile(compare_id, compare_file)
    
    total = 0
    worse = 0
    with open(compare_file) as compare_f:
        for line in compare_f:
            toks = line.split(', ')
            total += 1
            if int(toks[1]) < 0:
                worse += 1
                
    portion = float(worse) / float(total) if total > 0 else 0
    return total, portion

def run_mapeval(job, context, options, xg_file_ids, xg_comparison_ids, gcsa_file_ids, gbwt_file_ids,
                id_range_file_ids, snarl_file_ids,
                vg_file_ids, gam_file_ids, reads_gam_file_id, reads_xg_file_id, reads_bam_file_id,
                reads_fastq_file_ids,
                fasta_file_id, bwa_index_ids, bam_file_ids,
                pe_bam_file_ids, true_read_stats_file_id):
    """
    Main Toil job, and main entrypoint for use of vg_mapeval as a library.
    
    Run the analysis on the given files.
    
    TODO: Refactor to use a list of dicts/dict of lists for the indexes.
    
    Returns a pair of the position comparison results and the score comparison
    results.
    
    Each result set is itself a pair, consisting of a list of per-graph file
    IDs, and an overall statistics file ID.

    If evaluation is skipped (options.skip_eval is True), returns None instead
    and just runs the mapping.
    
    """
    
    # This should be the only Toil job that actually uses options (in order to
    # orchestrate the right shape of workflow depending on whether we want
    # particular analyses done).

    # Make an indexing job
    index_job = job.addChildJobFn(run_map_eval_index,
                                  context,
                                  xg_file_ids,
                                  gcsa_file_ids,
                                  gbwt_file_ids,
                                  id_range_file_ids,
                                  snarl_file_ids,
                                  vg_file_ids,
                                  cores=context.config.misc_cores,
                                  memory=context.config.misc_mem,
                                  disk=context.config.misc_disk)

    # Extract our truth positions if no true_read_stats_file_id
    if not true_read_stats_file_id and reads_gam_file_id:
        annotate_job = index_job.addChildJobFn(annotate_gam, context, reads_xg_file_id, reads_gam_file_id,
                                               memory=context.config.alignment_mem,
                                               disk=context.config.alignment_disk)
        true_read_stats_file_id = annotate_job.addFollowOnJobFn(extract_gam_read_stats,
                                                                context, 'truth', annotate_job.rv(),
                                                                disk=context.config.alignment_disk).rv()
    elif not true_read_stats_file_id and reads_bam_file_id:
        true_read_stats_file_id = index_job.addChildJobFn(extract_bam_read_stats,
                                                          context, 'truth', reads_bam_file_id, True,
                                                          disk=context.config.alignment_disk).rv()

    # Extract our fastq reads so that all aligners get the exact same inputs    
    # todo: should be able to use same reads, interleaved, for both
    fq_reads_ids_bwa = reads_fastq_file_ids
    if reads_fastq_file_ids and options.bwa:
        fq_reads_ids_bwa = index_job.addChildJobFn(run_strip_fq_ext, context, reads_fastq_file_ids,
                                                   disk=context.config.alignment_disk,
                                                   cores=context.config.alignment_cores).rv()
        
    fastq_fn = run_gam_to_fastq if reads_gam_file_id else run_bam_to_fastq
    fq_reads_ids, fq_paired_reads_ids, fq_paired_reads_for_vg_ids = (
        reads_fastq_file_ids, fq_reads_ids_bwa, reads_fastq_file_ids)
    
    # if we got two input fastqs, merge them together for single end
    if len(fq_reads_ids) == 2 and not options.paired_only:
        fq_reads_ids = [index_job.addChildJobFn(run_concat_fastqs, context, fq_reads_ids,
                                               disk=context.config.alignment_disk).rv()]
    
    if reads_gam_file_id or reads_bam_file_id:
        # There are reads to extract to FASTQ for realigning
    
        if not options.paired_only and not fq_reads_ids:
            fq_reads_ids = index_job.addChildJobFn(fastq_fn, context,
                                                   reads_gam_file_id if reads_gam_file_id else reads_bam_file_id,
                                                   False,
                                                   disk=context.config.alignment_disk).rv()
        if not options.single_only and not fq_paired_reads_ids:
            fq_paired_reads_ids  = index_job.addChildJobFn(fastq_fn, context,
                                                           reads_gam_file_id if reads_gam_file_id else reads_bam_file_id,
                                                           True,
                                                           disk=context.config.alignment_disk).rv()
            # todo: smarter annotation so we don't need to make two input sets, one with _1 _2 with vg and one without for bwa
            fq_paired_reads_for_vg_ids = index_job.addChildJobFn(fastq_fn, context,
                                                                 reads_gam_file_id if reads_gam_file_id else reads_bam_file_id,
                                                                 True, True,
                                                                 disk=context.config.alignment_disk).rv()

    # Compose a condition matrix to specify what independent variable values to run in the alignment experiment
    matrix = {
        "aligner": ["vg"],
        "paired": [],
        "multipath": [],
        "gbwt": []
    }
    
    if not options.multipath_only:
        # Allow the single-path vg map aligner
        matrix["multipath"].append(False)
    if options.multipath or options.multipath_only:
        # Run the multipath vg mpmap aligner
        matrix["multipath"].append(True)
        
    if not options.paired_only:
        # Allow unpaired read mapping
        matrix["paired"].append(False)
    if not options.single_only:
        # Allow paired read mapping
        matrix["paired"].append(True)
        
    if gbwt_file_ids:
        # We have GBWTs to use
        for gbwt_penalty in options.gbwt_penalties:
            # We have explicit penalties
            matrix["gbwt"].append(gbwt_penalty)
        if len(options.gbwt_penalties) == 0:
            # We have no explicit penalties; use the default
            matrix["gbwt"].append(True)
        
    if (not gbwt_file_ids) or options.strip_gbwt:
        # We have no GBWTs or we want to run without them too
        matrix["gbwt"].append(False)
        
    if options.bwa:
        # Make sure to run the BWA aligner too
        matrix["aligner"].append("bwa")
    
    # Then after indexing, do alignment
    alignment_job = index_job.addFollowOnJobFn(run_map_eval_align, context, index_job.rv(),
                                               xg_comparison_ids,
                                               options.gam_names, gam_file_ids,
                                               fq_reads_ids, fq_paired_reads_ids, fq_paired_reads_for_vg_ids,
                                               fasta_file_id, bwa_index_ids, matrix,
                                               options.ignore_quals, options.surject)
                                               
    # Unpack the alignment job's return values
    # TODO: we're clobbering input values...
    (gam_names, gam_file_ids, xg_ids, vg_map_times, bwa_bam_file_ids, bwa_map_times, surjected_results) = (
         alignment_job.rv(0), alignment_job.rv(1), alignment_job.rv(2),
         alignment_job.rv(3), alignment_job.rv(4), alignment_job.rv(5),
         alignment_job.rv(6))

    # We make a root for comparison here to encapsulate its follow-on chain
    comparison_parent_job = Job()
    alignment_job.addFollowOn(comparison_parent_job)

    # Dump out the running times into map_times.tsv
    comparison_parent_job.addChildJobFn(run_write_map_times, context, gam_names, vg_map_times, bwa_map_times)

    if options.skip_eval:
        # Skip evaluation
        return None

    # Otherwise, do mapping evaluation comparison (the rest of the workflow)
    comparison_job = comparison_parent_job.addChildJobFn(run_map_eval_comparison, context, xg_ids,
                     gam_names, gam_file_ids, options.bam_names, bam_file_ids,
                     options.pe_bam_names, pe_bam_file_ids, bwa_bam_file_ids, surjected_results,
                     true_read_stats_file_id, options.mapeval_threshold, options.compare_gam_scores, reads_gam_file_id,
                     downsample_portion=options.downsample,
                     gbwt_usage_tag_gam_name=options.gbwt_baseline,
                     cores=context.config.misc_cores, memory=context.config.misc_mem,
                     disk=context.config.misc_disk)

    # Then do the R plotting
    
    # What do we plot together?
    plot_sets = parse_plot_sets(options.plot_sets)
    
    # Fetch out the combined TSV from the return value for summarizing/plotting
    lookup_job = comparison_parent_job.addFollowOnJobFn(lookup_key_path, comparison_job.rv(), [0, 1])
    position_stats_file_id = lookup_job.rv()
    summarize_job = lookup_job.addFollowOnJobFn(run_map_eval_summarize, context, position_stats_file_id, plot_sets,
                                                cores=context.config.misc_cores, memory=context.config.misc_mem,
                                                disk=context.config.misc_disk)

    return comparison_job.rv()
    
def lookup_key_path(job, obj, path):
    """
    
    Get the item at the given path of keys by repeated [] lookups in obj.
    
    Work around https://github.com/BD2KGenomics/toil/issues/2214
    
    """
    
    for key in path:
        obj = obj[key]
        
    return obj

def run_map_eval_summarize(job, context, position_stats_file_id, plot_sets):
    """
    
    Make the summary plots and tables, based on a single combined position
    stats TSV in position_stats_file_id.
    
    Returns a list of file name and file ID pairs for plots and tables.
    
    plot_sets is a data structure of collections of conditions to plot against
    each other, as produced by parse_plot_sets. The first condition in each
    plot set is used as the comparison baseline.
    
    """
    
    RealtimeLogger.info("Running summary for {}".format(plot_sets))
    
    # Do plots
    plot_job = job.addChildJobFn(run_map_eval_plot, context, position_stats_file_id, plot_sets,
        cores=context.config.misc_cores, memory=context.config.misc_mem,
        disk=context.config.misc_disk)
    # And tables
    table_job = job.addChildJobFn(run_map_eval_table, context, position_stats_file_id, plot_sets,
        cores=context.config.misc_cores, memory=context.config.misc_mem,
        disk=context.config.misc_disk)
        
    # Concat file lists
    merge_job = plot_job.addFollowOnJobFn(run_concat_lists, plot_job.rv(), table_job.rv(),
        cores=context.config.misc_cores, memory=context.config.misc_mem,
        disk=context.config.misc_disk)
    table_job.addFollowOn(merge_job)
    return merge_job.rv()
    
def run_map_eval_plot(job, context, position_stats_file_id, plot_sets):
    """
    
    Make the PR and QQ plots with R, based on a single combined position stats
    TSV in position_stats_file_id.
    
    The combined position stats TSV has one header line, and format:
    
    correct flag, mapping quality, tag list (or '.'), method name, read name (or '.'), weight (or 1)
    
    plot_sets is a data structure of collections of conditions to plot against
    each other, as produced by parse_plot_sets.
    
    outputs plots/plot-pr.svg, plots/plot-qq.svg, and plots/plot-roc.svg for
    the first set, and plots/plot-pr-1.svg, etc. for subsequent sets.
    
    Returns a list of pairs of tuples of plot basename, plot file ID, and plot file path.
    
    """
    
    RealtimeLogger.info('Starting plotting...')
    
    work_dir = job.fileStore.getLocalTempDir()

    position_stats_path = os.path.join(work_dir, 'position_stats.tsv')
    job.fileStore.readGlobalFile(position_stats_file_id, position_stats_path)

    out_plot_tuples = []
    
    for i, plot_set in enumerate(plot_sets):
        # For each set of graphs to plot together
        
        # Unpack plot_set
        plot_title, plot_conditions = plot_set
        
        for rscript in ['pr', 'qq', 'roc']:
            # For each kind of plot
            
            RealtimeLogger.info('Plotting {} for plot set {}'.format(rscript, i))
           
            # Make a file name to save the plot to.
            # Make sure to include the type of R script being run.
            plot_filename = title_to_filename('plot-{}'.format(rscript), i, plot_title, 'svg')
           
            script_path = get_vg_script(job, context.runner, 'plot-{}.R'.format(rscript), work_dir)
            cmd = ['Rscript', os.path.basename(script_path), os.path.basename(position_stats_path),
                   plot_filename]
            if plot_conditions is not None:
                # Subset to specific conditions. The R scripts know how to do it.
                cmd.append(','.join(plot_conditions))
                
                if plot_title is not None:
                    # Provide a title for the plot
                    cmd.append(plot_title)
            
            try:
                context.runner.call(job, cmd, work_dir = work_dir)
                out_plot_tuples.append((plot_filename,
                    context.write_output_file(job, os.path.join(work_dir, plot_filename),
                    os.path.join('plots', plot_filename))))
            except Exception as e:
                if rscript == 'roc':
                    RealtimeLogger.warning('plot-roc.R failed: {}'.format(str(e)))
                else:
                    # We insist that the R scripts execute successfully (except plot-roc)
                    raise e
            
    RealtimeLogger.info('Plotting complete')
    
    return out_plot_tuples
    
def run_map_eval_table(job, context, position_stats_file_id, plot_sets):
    """
    
    Make table TSVs of wrong/correct/improved read counts.
    
    The combined position stats TSV has one header line, and format:
    
    correct flag, mapping quality, tag list (or '.'), method name, read name (or '.'), weight (or 1)
    
    plot_sets is a data structure of collections of conditions to plot against
    each other, as produced by parse_plot_sets. The first condition in each
    plot set is used as the comparison baseline.
    
    outputs plots/table.tsv for the first set, and plots/table-1.svg, etc. for
    subsequent sets.
    
    Returns a list of pairs of table file name and table file ID.
    
    """
    
    RealtimeLogger.info('Downloading mapeval stats for table...')
    
    # Find our working directory and download the stats file
    work_dir = job.fileStore.getLocalTempDir()
    position_stats_path = os.path.join(work_dir, 'position_stats.tsv')
    job.fileStore.readGlobalFile(position_stats_file_id, position_stats_path)
   
    RealtimeLogger.info('Making mapeval summary table...')
   
    # Parse the table out into actual statistics.
    
    # This creates an empty stats dict for a condition
    dict_for_condition = lambda: {
        'wrong': 0, # Total wrong reads
        'wrongTagged': collections.Counter(), # Wrong reads with each observed tag, or None for no tags
        'wrong60': 0, # Wrong reads with MAPQ 60
        'wrong0': 0, # Wring reads with MAPQ 0
        'wrong>0': 0, # Wrong reads with nonzero MAPQ
        'correct': 0, # Total correct reads
        'correctTagged': collections.Counter(), # Correct reads with each observed tag, or None for no tags
        'correct0': 0, # Correct reads with MAPQ 0
        'correctMapqTotal': 0, # Total MAPQ of all correct reads, for averaging
        'wrongNames': set() # Names of all wrong reads (which should be in the 1000s to 10ks in size)
    }
    
    # This holds, by condition name, a bunch of stat values by stat name.
    condition_stats = collections.defaultdict(dict_for_condition)
    
    # This holds all observed tags
    known_tags = set()
    
    # We will need to drop the first line (a header)
    line_num = 0
    with open(position_stats_path) as stats_stream:
        # Open the stats file
        for line in tsv.TsvReader(stats_stream):
            # And read all the lines.
            
            if line_num == 0:
                # Skip the header
                line_num += 1
                continue
                
            line_num += 1
            
            if line_num % 1000000 == 0:
                RealtimeLogger.info('Processed {} alignments for table in {} conditions'.format(line_num, len(condition_stats)))
            
            # Line format is:
            # correct flag, mapping quality, tags, condition name, read name, count
            if len(line) == 0:
                # Skip blank
                continue
            
            # Everything else must have all the fields
            assert(len(line) >= 6)
            # Unpack
            correct, mapq, tags, condition, read, count = line[0:6]
            # And parse
            correct = (correct == '1')
            mapq = int(mapq)
            tags = [] if tags == '.' else tags.split(',')
            count = int(count)
            
            if tags == []:
                # No tags is a tag now
                known_tags.add(None)
            else:
                for tag in tags:
                    # Register observed tags
                    known_tags.add(tag)
            
            # Find the stats dict to update
            stats = condition_stats[condition]
            
            # Update stats
            # TODO: Make stats be lambda-defined instead of manual?
            if correct:
                stats['correct'] += count
                stats['correct0'] += (mapq == 0) * count
                stats['correctMapqTotal'] += mapq * count
                if tags == []:
                    stats['correctTagged'][None] += count
                else:
                    for tag in tags:
                        stats['correctTagged'][tag] += count
            else:
                stats['wrong'] += count
                stats['wrong60'] += (mapq == 60) * count
                stats['wrong0'] += (mapq == 0) * count
                stats['wrong>0'] += (mapq > 0) * count
                stats['wrongNames'].add(read)
                if tags == []:
                    stats['wrongTagged'][None] += count
                else:
                    for tag in tags:
                        stats['wrongTagged'][tag] += count
                
    # Now we have aggregated all the stats for all the conditions. We need to make the tables.
    
    # Sort the known tags
    known_tags = sorted(list(known_tags))
    if len(known_tags) == 1:
        # Everything is tagged the same way, so ignore tags.
        known_tags = []

    # Hold the list of file name and file ID pairs to return
    out_name_id_pairs = []
    
    for i, plot_set in enumerate(plot_sets):
        # For each set of graphs to look at together
        
        RealtimeLogger.info('Create table for plot set {}'.format(i))
        
        # Unpack plot_set
        plot_title, plot_conditions = plot_set
        
        # Make a file name to save the table to
        table_filename = title_to_filename('table', i, plot_title, 'tsv')
        
        if plot_conditions is None:
            # Special value for running everything together.
            # Make sure the plot set actually has names in it.
            plot_conditions = list(condition_stats.keys())
            
        assert(len(plot_conditions) > 0)
            
        # Decide on our baseline condition.
        # It will just be the first condition specified.
        baseline_condition = plot_conditions[0]
        
        # Start the output file.
        writer = tsv.TsvWriter(open(os.path.join(work_dir, table_filename), 'w'))
        header = ['Condition', 'Precision']
        for tag in known_tags:
            header.append('+{}'.format(tag))
            header.append('-{}'.format(tag))
            
        header.append('Reads')
        for tag in known_tags:
            header.append('+{}'.format(tag))
            header.append('-{}'.format(tag))
        
        header.append('Wrong')
        for tag in known_tags:
            header.append('+{}'.format(tag))
            header.append('-{}'.format(tag))
        
        header += ['at MAPQ 60', 'at MAPQ 0', 'at MAPQ >0', 'new vs. ' + baseline_condition, 'fixed vs. ' + baseline_condition,
                   'Avg. Correct MAPQ', 'Correct MAPQ 0']
        writer.list_line(header)
        
        for condition in plot_conditions:
            # For each condition to plot, look up its stats
            stats = condition_stats[condition]
            
            # Start a line with Condition
            line = [condition]
            # Then Precision
            try:
                line.append(float(stats['correct']) / (stats['wrong'] + stats['correct']))
            except ZeroDivisionError:
                line.append("NaN")
            # Then precisions with and without all tags
            for tag in known_tags:
                try:
                    # Report with tag only
                    line.append(float(stats['correctTagged'][tag]) / (stats['wrongTagged'][tag] + stats['correctTagged'][tag]))
                except ZeroDivisionError:
                    line.append("NaN")
                try:
                    # Report without tag
                    line.append(float(stats['correct'] - stats['correctTagged'][tag]) / 
                        ((stats['wrong'] - stats['wrongTagged'][tag]) + (stats['correct'] - stats['correctTagged'][tag])))
                except ZeroDivisionError:
                    line.append("NaN")
                
            
            # Then Reads
            line.append(stats['wrong'] + stats['correct'])
            # Then counts with and without all tags
            for tag in known_tags:
                # Report with tag only
                line.append(stats['wrongTagged'][tag] + stats['correctTagged'][tag])
                # Report without tag
                line.append((stats['wrong'] - stats['wrongTagged'][tag]) + (stats['correct'] - stats['correctTagged'][tag]))
            
            # Then Wrong reads
            line.append(stats['wrong'])
            # Then counts with and without all tags
            for tag in known_tags:
                # Report with tag only
                line.append(stats['wrongTagged'][tag])
                # Report without tag
                line.append(stats['wrong'] - stats['wrongTagged'][tag])
            # Then counts in different quality buckets
            line.append(stats['wrong60'])
            line.append(stats['wrong0'])
            line.append(stats['wrong>0'])
            
            # Sum up the reads wrong in this condition but not in the baseline
            new_vs_baseline = 0
            for read in stats['wrongNames']:
                if read not in condition_stats[baseline_condition]['wrongNames']:
                    new_vs_baseline += 1
            line.append(new_vs_baseline)
            
            # Sum up the reads wrong in the baseline but not in this condition
            fixed_vs_baseline = 0
            for read in condition_stats[baseline_condition]['wrongNames']:
                if read not in stats['wrongNames']:
                    fixed_vs_baseline += 1
            line.append(fixed_vs_baseline)
            
            # Compute average MAPQ of correct reads
            if stats['correct'] != 0:
                # Can do division
                avg_correct_mapq = float(stats['correctMapqTotal']) / stats['correct']
            else:
                avg_correct_mapq = None
            line.append(avg_correct_mapq)
            
            line.append(stats['correct0'])
            
            writer.list_line(line)
            
        # Now the file is done
        writer.close()
        
        # Save it
        out_name_id_pairs.append((table_filename, context.write_output_file(job, os.path.join(work_dir, table_filename),
            os.path.join('plots', table_filename))))
            
    RealtimeLogger.info('Tables complete')
            
    # Return our pairs of file names and file IDS
    return out_name_id_pairs

def run_write_map_times(job, context, gam_names, vg_map_times, bwa_map_times):
    """
    Make a table of running times (in seconds) for mapping.  These times do not include 
    toil-vg overhead like downloading and chunking
    """

    work_dir = job.fileStore.getLocalTempDir()
    times_path = os.path.join(work_dir, 'map_times.tsv')
    with open(times_path, 'w') as times_file:
        times_file.write('aligner\tmap time (s)\n')
        for name, map_time in zip(gam_names, vg_map_times):
            if map_time is not None:
                times_file.write('{}\t{}\n'.format(name, round(map_time, 5)))
        if bwa_map_times[0] is not None:
            times_file.write('bwa-mem\t{}\n'.format(round(bwa_map_times[0], 5)))
        if bwa_map_times[1] is not None:
            times_file.write('bwa-mem-pe\t{}\n'.format(round(bwa_map_times[1], 5)))

    context.write_output_file(job, times_path)

def make_mapeval_plan(toil, options):
    """
    Import all the necessary files form options into Toil.
    
    Keep the IDs under names in an argparse namespace that functions as a "plan"
    for the workflow.
    
    """
    
    # Make a plan
    plan = argparse.Namespace()
    
    start_time = timeit.default_timer()
            
    # Upload local files to the remote IO Store
    
    # Input vg data (either pre-aligned or to align against). Can be either .vg
    # (to index and align against) or .xg/.gcsa/.gcsa.lcp (to align against) or
    # .gam/.xg (pre-alligned, just annotate)
    plan.gam_file_ids = []
    if options.gams:
        for gam in options.gams:
            plan.gam_file_ids.append(toil.importFile(gam))

    plan.vg_file_ids = []
    if options.vg_graphs:
        for graph in options.vg_graphs:
            plan.vg_file_ids.append(toil.importFile(graph))

    plan.xg_file_ids = []
    plan.xg_comparison_ids = [] # optional override xg_file_ids for comparison
    plan.gcsa_file_ids = [] # list of gcsa/lcp pairs
    plan.gbwt_file_ids = []
    plan.id_range_file_ids = []
    plan.snarl_file_ids = []
    imported_xgs = {}
    if options.index_bases:
        for ib in options.index_bases:
            if ',' in ib:
                ib, cib = ib.split(',')[0], make_url(ib.split(',')[1])
            else:
                cib = ib
            imported_xgs[ib + '.xg'] = toil.importFile(ib + '.xg')
            plan.xg_file_ids.append(imported_xgs[ib + '.xg'])
            if cib and cib + '.xg' not in imported_xgs:
                imported_xgs[cib + '.xg'] = toil.importFile(cib + '.xg')
            plan.xg_comparison_ids.append(imported_xgs[cib + '.xg'])
            if not options.gams:
                plan.gcsa_file_ids.append(
                    (toil.importFile(ib + '.gcsa'),
                    toil.importFile(ib + '.gcsa.lcp')))
                    
                if options.use_gbwt:
                    try:
                        # If the file exists/imports successfully, we use it
                        plan.gbwt_file_ids.append(toil.importFile(ib + '.gbwt'))
                    except:
                        # If it doesn't exist, it won't import. And we want to
                        # tolerate absent GBWT indexes for some graphs (like
                        # primary) where haplotype data is unavailable
                        plan.gbwt_file_ids.append(None)
                        
                    
                if options.use_snarls:
                    try:
                        # If the file exists/imports successfully, we use it
                        plan.snarl_file_ids.append(toil.importFile(ib + '.snarls'))
                    except:
                        # If it doesn't exist, it won't import. And we want to
                        # tolerate absent snarl indexes for some graphs (like
                        # the sample graph positive control) where they aren't
                        # available.
                        plan.snarl_file_ids.append(None)
                    
                    
                # multiple gam outputs not currently supported by evaluation pipeline
                #if os.path.isfile(os.path.join(ib, '_id_ranges.tsv')):
                #    id_range_file_ids.append(
                #        toil.importFile(ib + '_id_ranges.tsv'))

    plan.reads_xg_file_id = None
    if options.gam_input_xg:
        if options.gam_input_xg in imported_xgs:
            plan.reads_xg_file_id = imported_xgs[options.gam_input_xg]
        else:
            plan.reads_xg_file_id = toil.importFile(options.gam_input_xg)
                    
    # Import input reads to be realigned
    if options.gam_input_reads:
        plan.reads_gam_file_id = toil.importFile(options.gam_input_reads)
    else:
        plan.reads_gam_file_id = None

    # Import input reads to be realigned
    if options.bam_input_reads:
        plan.reads_bam_file_id = toil.importFile(options.bam_input_reads)
    else:
        plan.reads_bam_file_id = None

    # Import input reads to be realigned        
    plan.reads_fastq_file_ids = []
    if options.fastq:
        for sample_reads in options.fastq:
            plan.reads_fastq_file_ids.append(toil.importFile(sample_reads))
                                
    # Input bwa data        
    plan.bam_file_ids = []
    if options.bams:
        for bam in options.bams:
            plan.bam_file_ids.append(toil.importFile(bam))
    plan.pe_bam_file_ids = []
    if options.pe_bams:
        for bam in options.pe_bams:
            plan.pe_bam_file_ids.append(toil.importFile(bam))
            
    plan.fasta_file_id = None
    plan.bwa_index_ids = None
    if options.fasta:
        plan.bwa_index_ids = dict()
        for suf in ['.amb', '.ann', '.bwt', '.pac', '.sa']:
            fidx = '{}{}'.format(options.fasta, suf)
            try:
                plan.bwa_index_ids[suf] = toil.importFile(fidx)
            except:
                logger.info('No bwa index found for {}, will regenerate'.format(options.fasta))
                plan.bwa_index_ids = None
                break
        if not plan.bwa_index_ids:
            plan.fasta_file_id = toil.importFile(options.fasta)
    if options.truth:
        plan.true_read_stats_file_id = toil.importFile(options.truth)
    else:
        plan.true_read_stats_file_id = None

    end_time = timeit.default_timer()
    logger.info('Imported input files into Toil in {} seconds'.format(end_time - start_time))
    
    return plan

def mapeval_main(context, options):
    """
    Run the mapeval workflow.
    """

    # Make sure the options are good
    validate_options(options)
    
    # How long did it take to run the entire pipeline, in seconds?
    run_time_pipeline = None
        
    # Mark when we start the pipeline
    start_time_pipeline = timeit.default_timer()

    t = copy.deepcopy(context)
    with context.get_toil(options.jobStore) as toil:
        if not toil.options.restart:

            # Import everything
            plan = make_mapeval_plan(toil, options)

            # Make a job to run the mapeval workflow, using all these various imported files.
            main_job = Job.wrapJobFn(run_mapeval,
                                     context, 
                                     options, 
                                     plan.xg_file_ids,
                                     plan.xg_comparison_ids,
                                     plan.gcsa_file_ids,
                                     plan.gbwt_file_ids,
                                     plan.id_range_file_ids,
                                     plan.snarl_file_ids,
                                     plan.vg_file_ids, 
                                     plan.gam_file_ids,
                                     plan.reads_gam_file_id,
                                     plan.reads_xg_file_id,
                                     plan.reads_bam_file_id,
                                     plan.reads_fastq_file_ids,
                                     plan.fasta_file_id, 
                                     plan.bwa_index_ids, 
                                     plan.bam_file_ids,
                                     plan.pe_bam_file_ids, 
                                     plan.true_read_stats_file_id)
                
            # Output files all live in the out_store, but if we wanted to we could export them also/instead.

            # Init the outstore
            init_job = Job.wrapJobFn(run_write_info_to_outstore, context, sys.argv)
            init_job.addFollowOn(main_job)

            # Run the root job
            toil.start(init_job)
        else:
            toil.restart()
            
    end_time_pipeline = timeit.default_timer()
    run_time_pipeline = end_time_pipeline - start_time_pipeline
 
    print("All jobs completed successfully. Pipeline took {} seconds.".format(run_time_pipeline))
    

#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Bio import SeqIO
from Bio import Entrez

import http.client
import random
import logging


def ncbi(kingdom, n_genomes):
    """download random genomes sequences from ncbi genomes with entrez eutils.

    Args:
        kingdom (string): the kingdom from which the sequences are from
        n_genomes (int): the number of genomes to download

    Returns:
        list: a list of genome records
    """
    logger = logging.getLogger(__name__)
    Entrez.email = ''
    Entrez.tool = 'InSilicoSeq'
    full_id_list = Entrez.read(Entrez.esearch(
        'genome', term='%s[Organism]' % kingdom, retmax=100000))['IdList']
    genomes = []
    n = 0
    logger.info('Searching for %s to download' % kingdom)
    while n < n_genomes:
        ident = random.choice(full_id_list)
        genome_info = Entrez.read(
            Entrez.esummary(db='genome', id=ident))[0]
        if genome_info['Assembly_Accession']:  # TODO: IndexError
            nucleotide_id = Entrez.read(Entrez.elink(
                dbfrom='genome',
                db='nucleotide',
                id=ident))[0]['LinkSetDb'][0]['Link'][0]['Id']
            nucleotide_info = Entrez.read(
                Entrez.esummary(db='nucleotide', id=nucleotide_id))[0]
            if not nucleotide_info['AccessionVersion'].startswith('NZ'):
                logger.info('Downloading %s'
                            % nucleotide_info['AccessionVersion'])
                genome_record = Entrez.efetch(
                    'nucleotide',
                    id=nucleotide_id,
                    rettype='fasta',
                    retmode='txt')
                try:
                    record = SeqIO.read(genome_record, 'fasta')
                    n_count = record.seq.count('N') + record.seq.count('n')
                    assert n_count / len(record) != 1.0
                except http.client.IncompleteRead as e:
                    logger.warning(
                        'Failed to read downloaded genome. Skipping')
                    continue
                except AssertionError as e:
                    logger.warning(
                        '%s only contains Ns. Skipping'
                        % nucleotide_info['AccessionVersion'])
                    continue
                genomes.append(record)
                n += 1
            else:
                logger.debug(
                    'Found %s but no record associated. Skipping'
                    % genome_info['Assembly_Accession'])
                continue
        else:
            logger.debug(
                'Organism with ID %s has no associated Assembly. Skipping'
                % ident)
            continue

    return genomes


def to_fasta(genomes, output):
    """Write genomes to a fasta file

    Take a list of genome records and write them to a fasta file named
    output_genomes.fasta

    Args:
        genomes (list): list of genome records
        output (string): the output file name

    Returns:
        str: the file name
    """
    logger = logging.getLogger(__name__)
    # define name of output files
    try:
        f = open(output, 'a')
    except (IOError, OSError) as e:
        logger.error('Failed to open output file: %s' % e)
        sys.exit(1)
    else:
        logger.info('Writing genomes to %s' % output)
        with f:
            for record in genomes:
                SeqIO.write(record, f, 'fasta')
    return output

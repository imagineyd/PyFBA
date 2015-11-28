import os
import sys

import PyFBA

__author__ = 'Rob Edwards'

# We want to find the path to the Biochemistry/SEED/ files. This is a relative path and is two levels above us
pyfbadir, tail = os.path.split(__file__)
pyfbadir, tail = os.path.split(pyfbadir)
SS_FILE_PATH = os.path.join(pyfbadir, "Biochemistry/SEED/Subsystems/SS_functions_Oct_2015.txt")


def suggest_reactions_from_subsystems(reactions, reactions2run, ssfile=SS_FILE_PATH, threshold=0, verbose=False):
    """
    Read roles and subsystems from the subsystems file (which has
    role, subsystem, classification 1, classification 2) and make
    suggestions for missing roles based on the subsystems that only have
    partial reaction coverage.

    :param threshold: The minimum fraction of the genes that are already in the subsystem for it to be added (default=0)
    :type threshold: float
    :param reactions: our reactions dictionary from parsing the model seed
    :type reactions: dict
    :param reactions2run: set of reactions that  we are going to run
    :type reactions2run: set
    :param ssfile: a subsystem file (really the output of dump_functions.pl on the seed machines)
    :type ssfile: str
    :param verbose: add additional output
    :type verbose: bool
    :return: a set of reactions that could be added to test for growth
    :rtype: set
    """

    if not os.path.exists(ssfile):
        sys.stderr.write("FATAL: The subsystems file {} does not exist from working directory {}.".format(ssfile, os.getcwd()) +
                         " Please provide a path to that file\n")
        return set()

    # read the ss file
    subsys_to_roles = {}
    roles_to_subsys = {}
    with open(ssfile, 'r') as sin:
        for l in sin:
            if l.startswith('#'):
                continue
            p = l.strip().split("\t")
            if p[1] not in subsys_to_roles:
                subsys_to_roles[p[1]] = set()
            if p[0] not in roles_to_subsys:
                roles_to_subsys[p[0]] = set()
            subsys_to_roles[p[1]].add(p[0])
            roles_to_subsys[p[0]].add(p[1])

    # now convert our reaction ids in reactions2run into roles
    # we have a hash with keys = reactions and values = set of roles
    reacts = PyFBA.filters.reactions_to_roles(reactions2run)

    # foreach subsystem we need to know the fraction of roles that are present
    ss_present = {}
    ss_roles = {}
    for r in reacts:
        for rl in reacts[r]:
            if rl in roles_to_subsys:
                for s in roles_to_subsys[rl]:
                    if s not in ss_present:
                        ss_present[s] = set()
                        ss_roles[s] = set()
                    ss_present[s].add(rl)
                    ss_roles[s].add(r)

    ss_fraction = {}
    for s in ss_present:
        ss_fraction[s] = 1.0 * len(ss_present[s]) / len(subsys_to_roles[s])

    if verbose:
        for s in ss_roles:
            print("{}\t{}\t{}".format(s, ss_fraction[s], ss_roles[s], "; ".join(ss_present)))

    # now we can suggest the roles that should be added to complete subsystems.
    suggested_ss = set()
    for s in ss_fraction:
        if ss_fraction[s] >= threshold:
            suggested_ss.add(s)

    if verbose:
        sys.stderr.write("Suggesting " + str(len(suggested_ss)) + " subsystems\n")

    # suggested_ss = {s for s, f in ss_fraction.items() if f>0}
    suggested_roles = set()
    for s in suggested_ss:
        for r in subsys_to_roles[s]:
            if r not in reactions2run:
                suggested_roles.add(r)

    if verbose:
        sys.stderr.write("Suggesting " + str(len(suggested_roles)) + " roles\n")

    # finally, convert the roles to reactions
    new_reactions = PyFBA.filters.roles_to_reactions(suggested_roles)

    if verbose:
        sys.stderr.write("Found " + str(len(new_reactions)) + " reactions\n")

    suggested_reactions = set()
    for rl in new_reactions:
        suggested_reactions.update(new_reactions[rl])

    if verbose:
        sys.stderr.write("Suggested reactions is " + str(len(suggested_reactions)) + "\n")

    suggested_reactions = {r for r in suggested_reactions if r in reactions and r not in reactions2run}

    if verbose:
        sys.stderr.write("Suggested reactions is " + str(len(suggested_reactions)) + "\n")

    return suggested_reactions
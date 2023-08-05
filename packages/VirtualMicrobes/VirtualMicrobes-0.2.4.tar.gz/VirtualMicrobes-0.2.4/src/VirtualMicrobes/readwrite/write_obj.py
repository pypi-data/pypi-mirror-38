
'''
Writes plain text files that can be used to generate VirtualMicrobes.Cell objects or VirtualMicrobes.Environment objects.

The cell file is an accurate representation, containing everything to clone a VirtualMicrobes.Cell, and
can be used to start the simulation, or to do competition experiments.

The environment file contains not only the reaction universe, but also the influx rates, the grid size,
and the molecule properties.

(write_obj.py is complementary to read_obj.py)
'''

def string_to_file(string, filename):
    '''
    Writes stringrepresentation of object to a file
    '''
    f = open(filename, 'w')
    f.write(string)
    f.close()

def write_env(environment, filename = None):
    '''
    Makes string representation of a environment object.

    If no filename is given, it just returns the string.
    Otherwise, the file is written to <save_dir>/<filename>
    (default = <save_dir>/environment.env)
    '''
    out=""
    out+= '<molecules>\n'

    for rclass in environment.resource_classes.values():
        out+= rclass.short_repr() + '\n'
        for mol in rclass.molecules.values():
            out+= mol.short_repr() + '\n'
    for eclass in environment.energy_classes.values():
        out+= eclass.short_repr() + '\n'
        for mol in eclass.molecules.values():
            out+= mol.short_repr()+'\n'
    out+='<conversion reactions>\n'
    for c in environment.conversions:
        out+= c.short_repr()+'\n'
    out+=  '<transport reactions>\n'
    for t in environment.transports:
        out+=  t.short_repr()  +'\n'
    out+= '<degradation rates>\n'
    for mol_ext in environment.external_molecules:
        out+= mol_ext.name +'='+str(environment.degradation_dict[mol_ext])+'\n'
    out+= '<membrane diffusion rates>\n'
    for mol_ext in environment.external_molecules:
        out+= mol_ext.name +'='+str(environment.membrane_diffusion_dict[mol_ext])+'\n'
    out+= '<grid>\n'
    rows = environment.params.grid_rows
    cols = environment.params.grid_cols
    subrows = environment.params.grid_sub_div.row
    subcols = environment.params.grid_sub_div.col
    out+= 'rows='+str(rows)
    out+= ',cols='+str(cols)
    out+='\n'
    out+= 'subrows='+str(subrows)
    out+= ',subcols='+str(subcols)
    out+='\n'
    num = 0
    for sub in environment.subenvs:
        if num+1 > rows*cols: break
        out+='influx'+str(num)+':'
        num+=1
        influxlist = []
        for mol_ext, influx in sub.influx_dict.items():
            influxlist+=[mol_ext.name+'='+str(influx)]
        out+=','.join(influxlist)
        out+='\n'

    if filename is not None:
        print "saving stringrepresentation of env in", filename
        string_to_file(out,filename)
    else:
        print "\n\n\n\n\n\n\n NOT saving stringrepresentation of env in\n\n\n\n\n\n", filename
        return out

def write_cell(cell, filename = None, alive = False):
    '''
    Makes string representation of a cell object.
    The cell's properties are taken as they were at birth.

    If no filename is given, it just returns the string.
    Otherwise, the file is written to <save_dir>/<filename>
    (default = <save_dir>/data/best_dat/generation_bests<time>.cell)

    '''
    out=""
    unique_gene_id = 0
    unique_ids = dict()
    metabolic_genes = ['enz','pump']
    out+= '# This is a cell representation. Be careful to retain the structure in terms of brackets/spaces etc, as not every fallback is accounted for\n'
    out+= '<genes>\n'

    for mol in cell.small_mols:
        cell.set_small_mol_conc(mol, cell.get_small_mol_conc(mol))
    for gene_prod in cell.gene_products:
        cell.set_gene_prod_conc(gene_prod, cell.get_gene_prod_conc(gene_prod))

    for gene in cell.molecules["gene_products"]:
        unique_gene_id += 1
        reaction = ''
        if gene["type"] in metabolic_genes:
            reaction = ',reaction:' + gene.reaction.short_repr()
        else:
            reaction = ',reaction:None'

        out+= ('[id:'+str(gene.id) + ','
                + 'concentration:' + str(cell.molecules['gene_products'][gene].concentration)
                + reaction+'],' + str(gene) + '\n'
                )
        unique_ids[gene] = unique_gene_id

    out+= '<genome>\n'
    for i, chrom in enumerate(cell.genome.chromosomes):
        out+= 'chrom'+str(i)+':'
        for gene in chrom:
            out+= ' ' + str(gene.id)
        out += '\n'

    out+= '<molecule_concs>\n'
    mollist = []
    for mol,mol_str in cell.molecules["small_molecules"].items():
        mollist+= [mol.name+'='+str(mol_str.concentration)]
    out+='\n'.join(mollist)

    out+= '\n<cell_properties>\n'
    out += 'volume='+str(cell.volume)+'\n'
    out += 'raw_production='+str(cell.raw_production)+'\n'
    out += 'pos_production='+str(cell.pos_production)+'\n'
    out += 'raw_production_change_rate='+str(cell.raw_production_change_rate)+'\n'
    out += 'toxicity='+str(cell.toxicity)+'\n'
    out += 'toxicity_change_rate='+str(cell.toxicity_change_rate)+'\n'
    out += 'raw_death_rate='+str(cell.raw_death_rate)+'\n'
    out += 'alive='+str(alive)+'\n'
    out += 'divided='+str(cell.divided)+'\n'
    out += 'wiped='+str(cell.wiped)+'\n'
    out += 'iterage='+str(cell.iterage)+'\n'
    out += 'lineage='+str(cell.marker_dict['lineage'])+'\n'
    out += 'time_birth='+str(cell.time_birth)+'\n'
    out += 'unique_key='+str(cell._unique_key)+'\n'
    for parent in cell.parents:
        out += 'parent_key='+parent._unique_key+'\n'
    out += 'version='+str(cell.version)
    out += '\n<point_mutations> (' + str(len(cell.point_mut)) + ')\n'
    for mut in cell.point_mut:
        newval = mut.new_val if mut.par not in ['ligand_ks', 'ene_ks', 'subs_ks'] else ';'.join(map(str, [m for m in mut.new_val.values()]))
        out += str(mut.genomic_target.id)+';'+str(mut.par)+';'+str(newval)+'\n'
    out += '<sequence_mutations> (' + str(len(cell.sequence_mut)) + ')\n'
    for mut in cell.sequence_mut:
        out += str(mut.genomic_target.id)+';'+str(mut.par)+';'+str(mut.new_val)+'\n'
    out += '<chromosomal_mutations> (' + str(len(cell.chromosomal_mut)) + ')\n'
    for mut in cell.chromosome_dup:
        out += str(mut.genomic_target.id)+' duplicated\n'
    for mut in cell.chromosome_del:
        out += str(mut.genomic_target.id)+' deleted\n'
    for mut in cell.chromosome_fission:
        out += str(mut.genomic_target.id) + ' split up into ' + ','.join([str(m.id) for m in mut.post_mutation])+'\n'
    for mut in cell.chromosome_fusion:
        out += str(mut.genomic_target[0].id) + ' and ' +str(mut.genomic_target[1].id)+ ' fused into ' + str(mut.post_mutation.id)+'\n'
        #out += 'point(seq):'+str(mut.genomic_target)+';'+str(mut.par)+';'+str(newval)
    out += '<stretch_mutations> (' + str(len(cell.stretch_mut)) + ')\n'
    for mut in cell.tandem_dup:
        out += ' '.join([str(g.id) for g in mut.stretch]) + ' duplicated\n'
    for mut in cell.stretch_del:
        out += ' '.join([str(g.id) for g in mut.stretch]) + ' deleted\n'
    for mut in cell.translocate:
        out += ' '.join([str(g.id) for g in mut.stretch]) + ' translocated\n'
    for mut in cell.stretch_invert:
        out += ' '.join([str(g.id) for g in mut.stretch]) + ' inverted\n'
    out += '<horizontal_transfer> (' + str(len(cell.inherited_hgt['internal'])) + ')\n'
    for mut in cell.inherited_hgt['internal']:
        out += ' '.join([str(g.id) for g in mut.stretch]) + ' transfered\n'
    out += '<gene_discoveries> (' + str(len(cell.inherited_hgt['external'])) + ')\n'
    for mut in cell.inherited_hgt['external']:
        out += ' '.join([str(g.id) for g in mut.stretch]) + ' discovered\n'

    if filename is not None:
        string_to_file(out,filename)
    else:
        print "NOT saving stringrepresentation of cell.. are you sure? \n\n", filename
        return out

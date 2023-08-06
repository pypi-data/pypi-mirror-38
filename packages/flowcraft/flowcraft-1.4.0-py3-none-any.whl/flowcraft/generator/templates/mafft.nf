process mafft_{{ pid }} {

    {% include "post.txt" ignore missing %}

    tag { 'mafft' }

    publishDir "results/alignment/mafft_{{ pid }}/"

    input:
    file(assembly) from {{ input_channel }}.map{ it[1] }.collect()
    file(refs) from _ref_seqTyping.collect().unique()

    output:
    file ("*.align") into {{ output_channel }}
    {% with task_name="mafft", sample_id="val('single')" %}
    {%- include "compiler_channels.txt" ignore missing -%}
    {% endwith %}

    script:
    """



    cat ${assembly} ${refs} > all_assemblies.fasta

    mafft --adjustdirection --thread $task.cpus --auto all_assemblies.fasta > ${workflow.scriptName}.align
    """

}

{{ forks }}
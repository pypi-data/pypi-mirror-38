from django.contrib import admin
from django import forms
from .models import Region, IlluminaMethylation450, CpGHasTranscriptRegions


class RegionAdminForm(forms.ModelForm):
    class Meta:
        model = Region
        fields = '__all__'


class RegionAdmin(admin.ModelAdmin):
    form = RegionAdminForm
    list_display = ['name']
    readonly_fields = ['name']


admin.site.register(Region, RegionAdmin)


class IlluminaMethylation450AdminForm(forms.ModelForm):
    class Meta:
        model = IlluminaMethylation450
        fields = '__all__'


class IlluminaMethylation450Admin(admin.ModelAdmin):
    form = IlluminaMethylation450AdminForm
    list_display = ['ilmnid', 'name', 'addressa_id', 'allelea_probeseq', 'addressb_id',
                    'alleleb_probeseq',
                    'infinium_design_type', 'next_base', 'color_channel', 'forward_sequence',
                    'genome_build', 'chr',
                    'mapinfo', 'sourceseq', 'chromosome_36', 'coordinate_36', 'strand',
                    'probe_snps', 'probe_snps_10',
                    'random_loci', 'methyl27_loci', 'ucsc_refgene_name',
                    'ucsc_refgene_accession', 'ucsc_refgene_group',
                    'ucsc_cpg_islands_name', 'relation_to_ucsc_cpg_island', 'phantom',
                    'dmr', 'enhancer', 'hmm_island',
                    'regulatory_feature_name', 'regulatory_feature_group', 'dhs']
    readonly_fields = ['ilmnid', 'name', 'addressa_id', 'allelea_probeseq',
                       'addressb_id', 'alleleb_probeseq',
                       'infinium_design_type', 'next_base', 'color_channel',
                       'forward_sequence', 'genome_build', 'chr',
                       'mapinfo', 'sourceseq', 'chromosome_36', 'coordinate_36',
                       'strand', 'probe_snps',
                       'probe_snps_10', 'random_loci', 'methyl27_loci',
                       'ucsc_refgene_name', 'ucsc_refgene_accession',
                       'ucsc_refgene_group', 'ucsc_cpg_islands_name',
                       'relation_to_ucsc_cpg_island', 'phantom', 'dmr',
                       'enhancer', 'hmm_island', 'regulatory_feature_name',
                       'regulatory_feature_group', 'dhs']


admin.site.register(IlluminaMethylation450, IlluminaMethylation450Admin)


class CpGHasTranscriptRegionsAdminForm(forms.ModelForm):
    class Meta:
        model = CpGHasTranscriptRegions
        fields = '__all__'


class CpGHasTranscriptRegionsAdmin(admin.ModelAdmin):
    form = CpGHasTranscriptRegionsAdminForm


admin.site.register(CpGHasTranscriptRegions, CpGHasTranscriptRegionsAdmin)

from . import models
from . import serializers
from . import utils

from django.db.models import Q
from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied


class GenomeViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for the Genome class"""
    queryset = models.Genome.objects.all()
    serializer_class = serializers.GenomeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        assembly = self.request.query_params.get('assembly', None)

        if assembly:
            return self.queryset.filter(assembly=assembly)

        return self.queryset


class ChromosomeViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for the Chromosome class"""

    queryset = models.Chromosome.objects.all()
    serializer_class = serializers.ChromosomeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        assembly = self.request.query_params.get('assembly', None)
        name = self.request.query_params.get('name', None)

        if not assembly:
            raise PermissionDenied()

        if name:
            return self.queryset.filter(name=name)

        return self.queryset


class GeneViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for the Gene class"""

    queryset = models.Gene.objects.all()
    serializer_class = serializers.GeneSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        assembly = self.request.query_params.get('assembly', None)
        chr = self.request.query_params.get('chr', None)
        name = self.request.query_params.get('name', None)

        if not assembly:
            raise PermissionDenied()

        self.queryset = self.queryset.filter(chromosome__genome__assembly=assembly)

        if chr:
            chr_query, txstart, txend = utils.get_coordinates_chr(chr)
            if chr_query and txstart and txend:
                return self.queryset.filter(Q(chromosome__name=chr_query),
                                            Q(genelocation__txend__lte=txend,
                                              genelocation__txend__gte=txstart) |
                                            Q(genelocation__txstart__lte=txend,
                                              genelocation__txstart__gte=txstart) |
                                            Q(genelocation__txstart__lte=txstart,
                                              genelocation__txend__gte=txend)).distinct()

        if chr and name:
            return self.queryset.filter(chromosome__name=chr, name=name)
        elif chr and not name:
            self.queryset = self.queryset.filter(chromosome__name=chr)
        elif not chr and name:
            self.queryset = self.queryset.filter(name=name)

        return self.queryset


class TranscriptViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for the Transcript class"""

    queryset = models.Transcript.objects.all()
    serializer_class = serializers.TranscriptSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        assembly = self.request.query_params.get('assembly', None)
        name = self.request.query_params.get('name', None)

        if not assembly:
            raise PermissionDenied()

        if name:
            self.queryset = self.queryset.filter(name=name)

        return self.queryset

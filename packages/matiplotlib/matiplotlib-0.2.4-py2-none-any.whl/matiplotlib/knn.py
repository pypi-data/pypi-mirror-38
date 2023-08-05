import pandas as pd


class Knn:

    def __init__(self, sample1, sample2, amostra_teste):
        self.sample1 = sample1
        self.sample2 = sample2
        self.series1 = pd.Series([*sample1])
        self.series2 = pd.Series([*sample2])
        self.amostra_teste = amostra_teste

    def table(self):
        media_sample1 = self._get_media(self.series1)
        desvio_padrao_sample1 = self._get_desvio_pad(self.series1)
        normalizacao_sample1 = self._normalize(
            media=media_sample1,
            desvio_padrao=desvio_padrao_sample1,
            sample=self.sample1
        )
        normalizacao_sample1.update({'amostra_teste_norm':  self._normalize(media_sample1, desvio_padrao_sample1, [self.amostra_teste[0]])})

        media_sample2 = self._get_media(self.series2)
        desvio_padrao_sample2 = self._get_desvio_pad(self.series2)
        normalizacao_sample2 = self._normalize(
            media=media_sample2,
            desvio_padrao=desvio_padrao_sample2,
            sample=self.sample2
        )
        normalizacao_sample2.update({'amostra_teste_norm': self._normalize(media_sample2, desvio_padrao_sample2, [self.amostra_teste[1]])})

        return {
            'sample1': {
                'media': media_sample1,
                'desvio_padrao': desvio_padrao_sample1,
                'normalizacao': normalizacao_sample1,

            },
            'sample2': {
                'media': media_sample2,
                'desvio_padrao': desvio_padrao_sample2,
                'normalizacao': normalizacao_sample2
            },
            'distancia': self._distancia(normalizacao_sample1, normalizacao_sample2)

        }

    def _get_media(self, series):
        return series.mean()

    def _get_desvio_pad(self, series):
        return series.std()

    def _normalize(self, media, desvio_padrao, sample):
        padrao_norm = {}
        nums = []
        for idx, valor in enumerate(sample):
            nums.append(valor)
            normalizado = (valor - media)/desvio_padrao
            padrao_norm.update({idx: normalizado})

        padrao_norm.update({'media': pd.Series([*nums]).mean()})
        padrao_norm.update({'desvio': pd.Series([*nums]).std()})

        return padrao_norm

    def _distancia(
        self,
        normalizacao1,
        normalizacao2
    ):
        distancia = {}
        for idx, value in normalizacao1.items():
            if str(idx) not in ('amostra_teste_norm'):
                distancia.update({idx: (value - normalizacao1['amostra_teste_norm'][0]) **2 + (normalizacao2[idx] - normalizacao2['amostra_teste_norm'][0]) **2})

        return distancia

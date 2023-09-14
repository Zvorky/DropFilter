# <p align="center"><img src="https://github.com/Zvorky/DropFilter/blob/main/ArtWork/DropFilter_icon.svg" width="44" height="44"> DropFilter</p>

O DropFilter é um projeto em Python que simplifica a organização e movimentação de arquivos em um diretório com base em critérios de filtragem personalizáveis. Esta ferramenta oferece uma maneira eficiente de gerenciar seus arquivos, ajudando a manter a ordem no seu sistema de arquivos.

----

### <p align="center">Recursos Principais</p>

- **Filtragem de Arquivos Personalizável:** O DropFilter permite que você configure regras de filtragem com base em vários critérios, como nome de arquivo, tipo e extensão.

- **Organização Automática:** Os arquivos que correspondem aos critérios de filtragem são movidos automaticamente para diretórios específicos, simplificando a organização dos seus arquivos.

- **Configuração Flexível:** Você pode personalizar regras de filtragem, diretórios de destino e outros parâmetros no arquivo de configuração.

- **Notificações e Registros:** O DropFilter fornece notificações e registros detalhados para mantê-lo informado sobre as ações realizadas.

----

### <p align="center">Uso Básico</p>

1. Após executar o DropFilter, ele irá gerar um arquivo de configuração padrão em .config/dropfilter.
2. Edite o arquivo config.json conforme desejar e salve-o.
3. O DropFilter irá recarregar automaticamente o arquivo de configuração, começando a monitorar o diretório especificado e organizando automaticamente os arquivos com base nas suas configurações.

----

### <p align="center">Exemplo de Configuração</p>

Você pode definir regras de filtragem e diretórios de destino no arquivo de configuração JSON:

```json
{
  "SleepTime": 20,
  "File": {
    "Any": {
      "Contains": [""]
    },
    "Code": {
      "Ends": [".cpp", ".h", ".py", ".sh"]
    },
    "PDF": {
      "Ends": [".pdf"]
    },
    "Video": {
      "Ends": [".mp4", ".mkv", ".webm", ".mov"]
    }
  },
  "Directory": {
    "Dropbox": "/home/user/Dropbox",
    "Desktop": "/home/user/Desktop",
    "Downloads": "/home/user/Downloads",
    "PDF_DL": "/home/user/Downloads/PDF"
  },
  "Filter": [
    {
      "walk": [["Downloads"], "PDF", "PDF_DL"]
    },
    {
      "Only": [["Desktop"], "Code", "Dropbox"]
    }
  ]
}
```

#

**Observação:** Certifique-se de que a biblioteca `gi.repository` e as dependências necessárias estejam instaladas para que o DropFilter funcione corretamente.

O DropFilter é uma ferramenta versátil que ajuda na organização e no gerenciamento eficiente de arquivos. Personalize suas configurações e deixe o DropFilter cuidar da organização de arquivos para você.

# Automação de Marcação de Ocorrências – VCOM

Este projeto automatiza o processo de **geração, filtragem e importação de ocorrências no sistema VCOM**, reduzindo tarefas manuais e garantindo maior agilidade no processamento de contratos.

A automação combina **tratamento de dados em Excel**, **integração com banco SQL para execução de macros**, e **automação web para interação direta com o sistema VCOM**, permitindo que todo o fluxo seja executado automaticamente através de uma interface gráfica.

## 🎯 Objetivo

Automatizar etapas operacionais que antes eram feitas manualmente, como:

- leitura e tratamento de bases em Excel
- aplicação de filtros e regras de negócio
- geração de arquivos de carga
- execução de **macros via integração SQL**
- importação automática no sistema **VCOM**
- acompanhamento da execução em tempo real


## 🌐 Automação Web

O projeto inclui uma rotina de **automação web responsável pela interação com o sistema VCOM**, realizando automaticamente:

- login no sistema
- navegação entre páginas
- importação de arquivos gerados
- execução das rotinas operacionais necessárias

Essa etapa elimina a necessidade de realizar essas ações manualmente no sistema.

## 🧠 Integração com SQL

Além do processamento de dados, o sistema também possui **integração com SQL**, utilizada para:

- executar consultas auxiliares
- suportar rotinas utilizadas por **macros do Excel**
- complementar o processamento das bases utilizadas na automação


## 🖥️ Interface Gráfica (`app.py`)

O projeto possui uma interface moderna desenvolvida com **CustomTkinter**, permitindo executar a automação de forma simples e visual.

A interface oferece:

- seleção do tipo de base a ser processada
- **logs em tempo real** exibindo cada etapa da execução
- **barra de progresso**
- **indicador visual de processamento**
- **botão de alternância entre modo claro e modo noturno**
- execução da automação sem travar a interface (uso de threads)

Isso permite acompanhar o processamento **ao vivo**, facilitando monitoramento e diagnóstico.

## 🧰 Tecnologias Utilizadas

- **Python 3**
- **Pandas** – tratamento e manipulação de dados
- **SQL** – suporte a consultas e execução de macros
- **Excel** – entrada e saída de dados
- **CustomTkinter** – interface gráfica
- **Automação Web** – integração com o sistema VCOM
- **Threading** – execução sem travar a interface

---

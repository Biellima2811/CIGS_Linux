# 🖥️ C.I.G.S — Central de Operações Linux

> Automação de deploy de WARs e gerenciamento do Tomcat em servidores
> Linux (Ubuntu Server / CentOS / Oracle Linux), com agendamento
> remoto, controle de acesso por desafio-resposta e logs de auditoria.

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Linux%20x86__64-orange.svg)]()
[![Build](https://img.shields.io/badge/Build-PyInstaller-4B8BBE.svg)](https://pyinstaller.org/)
[![License](https://img.shields.io/badge/License-Internal-lightgrey.svg)]()

---

## 📑 Índice

- [Visão Geral](#-visão-geral)
- [Funcionalidades](#-funcionalidades)
- [Arquitetura](#-arquitetura)
- [Pré-requisitos](#-pré-requisitos)
- [Instalação no Servidor](#-instalação-no-servidor)
- [Uso Diário (Operação)](#-uso-diário-operação)
- [Compilação do Binário](#-compilação-do-binário)
- [Segurança](#-segurança)
- [Estrutura de Pastas](#-estrutura-de-pastas)
- [Logs e Auditoria](#-logs-e-auditoria)
- [Troubleshooting](#-troubleshooting)
- [Roadmap](#-roadmap)
- [Licença](#-licença)

---

## 🎯 Visão Geral

O **CIGS** (Central de Operações Linux) é a evolução de um script
Bash monolítico (`operacao_tatica.sh`) usado para distribuir
atualizações de WAR entre múltiplos clientes de uma instalação
Tomcat.

Foi reescrito em **Python 3** com foco em:

- **Robustez** — tratamento explícito de erros, sem `exit 1` seco.
- **Auditabilidade** — logs estruturados com timestamp e nível.
- **Operação contínua** — menu em loop (o Bash exigia reabrir a cada ação).
- **Distribuição segura** — binário compilado, código-fonte não exposto.
- **Manutenibilidade** — arquitetura orientada a objetos com
  responsabilidade única por módulo.

### Fluxo de alto nível

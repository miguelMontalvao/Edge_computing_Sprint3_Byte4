# Sistema de Monitoramento Termo-Higrométrico de Borda para Treinamento de Alta Performance (Pelé Academia)

## 1. Visão Geral do Projeto

Este projeto consiste em um protótipo de **Edge Computing** (Processamento na Borda) desenvolvido para a **Pelé Academia** (Resende FC). A aplicação visa monitorar, em tempo real, as condições ambientais de temperatura e umidade relativa do ar nos centros de preparação física, fisioterapia e fortalecimento muscular da academia.

O ecossistema utiliza o microcontrolador **ESP32** para aquisição de dados via sensor de temperatura e umidade, realizando o processamento local (filtragem e cálculo de média móvel das medições) e exibindo o status operacional por meio de uma Interface Homem-Máquina (IHM) local. Além disso, o dispositivo transmite a telemetria via Wi-Fi para a plataforma em nuvem **ThingSpeak**, viabilizando o histórico e a análise gráfica remota.

---

## 2. Fundamentação Científica e Justificativa

Em atletas de alto rendimento, o ambiente térmico desempenha um papel determinante na eficiência metabólica, no estresse cardiovascular e na prevenção de lesões musculares.

De acordo com o **Colégio Americano de Medicina do Esporte (ACSM - *American College of Sports Medicine*)** e diretrizes da **Organização Mundial da Saúde (OMS)**, a faixa ideal de conforto térmico para a prática de exercícios físicos em ambientes fechados situa-se entre **18 °C e 23 °C**, com **Umidade Relativa do Ar (UR) entre 40% e 60%**.

* **Temperaturas acentuadas (> 25 °C)** ou **Alta Umidade (> 60%)**: Dificultam a dissipação do calor corporal por meio da evaporação do suor, resultando em elevação prematura da frequência cardíaca, risco de estresse térmico (*heat stress*) e fadiga precoce.
* **Temperaturas reduzidas (< 18 °C)** ou **Baixa Umidade (< 40%)**: Podem ocasionar vasoconstrição periférica, rigidez muscular, ressecamento das vias aéreas superiores e maior suscetibilidade a lesões em treinos de potência.

Dessa forma, o processamento de borda auxilia na manutenção proativa da climatização dos espaços de treino, fornecendo feedback imediato para a comissão técnica e preparados físicos.

---

## 3. Arquitetura da Solução e Divisão das Operações

A solução divide o processamento entre a borda (*Edge*) e a nuvem (*Cloud*), otimizando o consumo de banda de rede e a latência de resposta.

```
+-----------------------------------------------------------------------+
|                             EDGE COMPUTING                            |
|                                                                       |
|  +------------------+     +-------------------+     +--------------+  |
|  |  Sensor DHT22    | --> |  ESP32            | --> |  Display LCD |  |
|  |  (Temp & Umid)   |     |  - Média Móvel    |     |  I2C (16x2)  |  |
|  +------------------+     |  - Classificação  |     +--------------+  |
|                           +-------------------+                       |
+-------------------------------------|---------------------------------+
                                      | Wi-Fi (HTTP GET)
                                      v
+-----------------------------------------------------------------------+
|                            CLOUD COMPUTING                            |
|                                                                       |
|  +-----------------------------------------------------------------+  |
|  |                       Plataforma ThingSpeak                     |  |
|  |  - Armazenamento Histórico                                      |  |
|  |  - Análise Gráfica Pública                                    |  |
|  +-----------------------------------------------------------------+  |
+-----------------------------------------------------------------------+
```

### Operações Realizadas Localmente (Edge Computing - ESP32)
1. **Aquisição Periódica de Dados**: Leitura periódica do sensor DHT22.
2. **Processamento e Filtragem (Média Móvel)**: Implementação de um buffer circular com as últimas 5 medições de temperatura e umidade, atenuando ruídos e flutuações momentâneas de leitura.
3. **Lógica de Decisão e Alertas**: Avaliação contínua da média móvel contra as faixas limítrofes predefinidas (`IDEAL`, `QUENTE`, `FRIO`, `AR SECO`, `AR HUMIDO`).
4. **Interface Homem-Máquina (IHM)**: Atualização imediata do display LCD 16x2 com formatação rigorosa de 16 caracteres por linha para evitar sobreposição ou falhas de leitura.

### Operações Realizadas na Nuvem (Cloud Computing - ThingSpeak)
1. **Telemetria e Persistência**: Recebimento de dados via protocolo HTTP GET a cada 15 segundos.
2. **Visualização Gráfica e Histórico**: Geração de gráficos públicos em tempo real para monitoramento remoto por gestores de infraestrutura da academia.

---

## 4. Recursos e Pinos Utilizados

| Componente | Tipo / Descrição | Pino no ESP32 | Protocolo / Sinal |
| :--- | :--- | :--- | :--- |
| **ESP32** | Microcontrolador Wi-Fi/Bluetooth | - | Unidade Central de Processamento |
| **DHT22** | Sensor de Temp. e Umidade | GPIO 15 | Sinal Digital Dedicado |
| **LCD 16x2 I2C** | Interface Homem-Máquina (IHM) | GPIO 21 (SDA)<br>GPIO 22 (SCL) | I2C (Endereço `0x27`) |

---

## 5. Estrutura de Arquivos no Repositório

O repositório deve conter obrigatoriamente a seguinte estrutura para execução no Wokwi em MicroPython:

* **`main.py`**: Código principal contendo a lógica de aquisição, cálculo da média móvel, IHM e integração ThingSpeak.
* **`lcd_api.py`**: Classe abstrata de manipulação e comandos de displays LCD.
* **`i2c_lcd.py`**: Driver de comunicação I2C para o display LCD no MicroPython.
* **`diagram.json`**: Mapeamento do circuito e esquemático das conexões no ambiente Wokwi.
* **`README.md`**: Documentação acadêmica e técnica completa do projeto.

---

## 6. Links do Projeto

* **Simulação Interativa (Wokwi)**: [Acessar Projeto no Wokwi](https://wokwi.com/projects/476000106480673793)
* **Canal Público de Telemetria (ThingSpeak)**: [Acessar Visualização Pública no ThingSpeak](https://thingspeak.mathworks.com/channels/3506596)

---

## 7. Instruções para Reprodução no Wokwi

1. Acesse o [Wokwi](https://wokwi.com/).
2. Crie um novo projeto selecionando **ESP32** com linguagem **MicroPython**.
3. Adicione os arquivos `lcd_api.py` e `i2c_lcd.py` no gerenciador de arquivos lateral.
4. Cole o código do `main.py` no arquivo correspondente.
5. Inicie a simulação.
6. Altere a temperatura e umidade no sensor DHT22 para verificar a reação do display LCD e a atualização no ThingSpeak.

---

## Referências Bibliográficas

* AMERICAN COLLEGE OF SPORTS MEDICINE (ACSM). **Exercise and Fluid Replacement**. Medicine & Science in Sports & Exercise, v. 39, n. 2, p. 377-390, 2007.
* WORLD HEALTH ORGANIZATION (WHO). **Thermal Environment and Health Aspects in Sports Practice**. Geneva: WHO, 2018.

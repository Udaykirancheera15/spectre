# Spectre: A Modular Robustness Evaluation Framework for LLM-Based Malware Traffic Classifiers

**Design Document – PhD-Level Research Blueprint**  
*Senior AI Security Researcher Perspective*

---

## 1. Overall Research Roadmap

**Vision**  
To establish a principled, extensible methodology for stress-testing LLM-based network traffic classifiers under realistic adversarial constraints, starting with evasion attacks and expanding toward a comprehensive benchmark for traffic analysis robustness.

**Phases**

- **Phase 0 — Foundational Classifier (Months 1–4)**  
  Build the best possible LLM-centric malware traffic classifier, optimizing the data representation, tokenization, and fine‑tuning pipeline. This phase yields the target model that Spectre will attack.

- **Phase 1 — Spectre Core & Evasion Engine (Months 4–8)**  
  Implement the Spectre framework with a modular attack/probe hierarchy. Deliver a fully functional evasion attack suite including a constraint‑aware mutation engine, evaluator, and reporting.

- **Phase 2 — Empirical Analysis & Benchmarking (Months 8–12)**  
  Run large‑scale evaluations, produce baseline robustness metrics, identify failure modes, and document the first Spectre benchmark dataset.

- **Phase 3 — Expansion & Hardening (Months 12–18)**  
  Add additional attack families (confidence manipulation, representation attacks, flow mutation, prompt attacks, etc.), extend the probe library, and refine the framework based on community feedback.

- **Phase 4 — Publication & Open‑Source Release (Months 18–24)**  
  Submit to a top‑tier security venue, release the full framework, datasets, and leaderboard.

---

## 2. Best Architecture for LLM-Based Malware Traffic Classification

After critical evaluation of conventional and hybrid designs, the recommended architecture is a **decoder-only LLM trained on a discretised, tokenised representation of packet-level sequences**, with a multi‑stage enrichment pipeline.

### Core Architecture

1. **Flow Segmentation & Feature Extraction**  
   Each bidirectional flow (5‑tuple) is extracted from the pcap using a fast C‑based tool (nfstream, joy, or custom). The flow is converted into a sequence of per‑packet feature vectors:  
   `[direction, packet_size, inter‑arrival_time_bin, TCP_flags_bitmask, IP_TTL, TLS_record_type (if available), DNS_opcode_bin, HTTP_method_id, …]`

2. **Tokenisation via Vector Quantization**  
   A learned codebook (VQ‑VAE or a simple embedding table with Gumbel‑Softmax) maps each packet‑level feature vector to a discrete token ID. The vocabulary size is intentionally small (256–1024) to keep sequences compact. This creates a “traffic language”.

3. **Flow Serialization**  
   Each flow is represented as a sequence of traffic tokens, optionally interleaved with special tokens marking direction changes, session initiation, or protocol transitions. Start and end‑of‑flow tokens are added.

4. **Decoder‑Only LLM Backbone**  
   A pre‑trained open‑source LLM (Llama‑3‑8B, Phi‑3‑mini, or DeepSeek‑V2‑Lite) is fine‑tuned to perform next‑token prediction on the traffic token sequences (if we also want generative capabilities) or, more simply, a classification head is attached to the last token’s hidden state. The classification variant is preferred for pure accuracy.

5. **Optional Hierarchical Extension**  
   For very long flows, a two‑stage architecture can summarise small packet chunks with a local transformer (e.g., a tiny 4‑layer encoder) and then feed these summary tokens to the LLM. This reduces context length while preserving global temporal dependencies.

### Why This Architecture?

- **Token Efficiency**: 50–500 tokens per flow (vs. thousands for raw text), allowing full‑flow context within the LLM’s window.
- **Adversarial Compatibility**: Perturbations applied at the packet level (timing, padding, fragmentation) directly translate into modified token sequences, enabling white‑box and black‑box robustness testing.
- **Transfer Learning**: The LLM’s pretrained attention mechanisms capture long‑range dependencies across packets, which classical flow‑based models (Random Forest, GRU) often miss.
- **Extensibility**: New protocol features are simply additional dimensions in the per‑packet vector, and the VQ codebook can be retrained without altering the LLM backbone.

**Rejected Alternatives & Weaknesses**

| Alternative | Weakness |
|------------|----------|
| Raw tshark/Wireshark text fed to LLM | Hugely token‑inefficient, uncontrollable noise, fails to scale to large datasets. |
| Zeek logs as natural language | Loses packet‑level timing and ordering resolution; LLM struggles with tabular‑like prose. |
| Statistical flow summaries (mean, std, etc.) | Discards sequential dependencies crucial for evasion detection. |
| Graph neural networks over flow graphs | Computationally heavy, not yet naturally paired with LLMs for joint reasoning. |
| Encoder‑only models (BERT) on fixed‑length sequences | Context fragmentation, limited to classification only, less flexible for future attack evaluation that might require generation. |

Thus the tokenised packet‑sequence approach represents a **genuinely novel** marriage of traffic processing and modern LLM capabilities.

---

## 3. Best Data Representation for LLMs

**Winner: Tokenised Packet Sequence with Learned Discrete Codebook**

Details:

- **Per‑Packet Feature Vector**  
  Select features that are robust to benign variability yet sensitive to adversarial manipulation. Candidate features:
  - Direction (2 bits: client→server / server→client)
  - Payload length (binned into 64 quantiles of flow‑specific empirical distribution)
  - TCP flags (syn, ack, fin, rst, psh, urg) as a 6‑bit mask
  - Inter‑arrival time (IAT) – log‑scaled and binned into 32 categories
  - IP TTL (raw, 0‑255)
  - Protocol‑specific: TLS record type (0‑23), DNS query type (0‑16), HTTP method (0‑9) – enumerated
  - Optional: entropy of payload first N bytes (binned)
  - Padding indicator (0/1) – whether the packet contains extra null bytes

- **Codebook Training**  
  Use a convolutional VQ‑VAE over mini‑batches of packet vectors from the entire training set. The encoder compresses a local context of 4 packets, quantizes, decoder reconstructs. The codebook size is set to 512. The quantized indices become the traffic tokens.

- **Sequence Structure**  
  `[FLOW_START] token_1 token_2 … token_N [FLOW_END]`  
  Optionally, insert `[DIR_CHANGE]` tokens when direction flips, which helps the LLM learn request‑response patterns.

- **Why not text?**  
  LLMs were not pretrained on network protocol dumps. Translating traffic into a controlled “language” via VQ yields a representation that the LLM can treat as a new domain during fine‑tuning, with minimal interference from irrelevant linguistic priors.

---

## 4. Best Fine‑Tuning Strategy

**Recommendation: Full parameter fine‑tuning of a small (3B–8B) decoder‑only model, preceded by a short continual pretraining phase on unlabelled traffic token sequences.**

| Component | Choice | Justification |
|-----------|--------|---------------|
| Continual pretraining | 1 epoch over 100M unlabelled traffic tokens (from benign + malware) | Adapts the LLM’s internal representations to the traffic domain without catastrophic forgetting. |
| Fine‑tuning | Full fine‑tuning on classification task | Maximum accuracy; LLMs under 8B can be fully trained on 4× A100 GPUs with DeepSpeed ZeRO‑3. |
| LoRA/QLoRA | Only for rapid prototyping; final model uses full FT | QLoRA leaves a performance gap when target domain is far from natural language. |
| Instruction tuning | Not needed for pure classification, but a multi‑task instruction format (“Classify this flow: …”) can later aid explanation generation. |
| Preference optimisation (DPO) | Applied after classification training to align the model’s confidence with human‑defined risk thresholds, reducing overconfidence under evasion. |
| Curriculum learning | Start with clean, full‑length flows; gradually introduce truncated, perturbed, or obfuscated traffic. This boosts robustness against evasion even before adversarial evaluation. |

**Context Length**  
The LLM’s native context window (8192 for Llama‑3) is more than sufficient; we will set a maximum flow length of 1024 traffic tokens (≈ 1024 packets) and pad/truncate.

**Tokenizer Considerations**  
We keep the original LLM tokenizer for the special tokens and add new tokens for the traffic codebook (IDs 0‑511). The embedding table is extended, and those rows are randomly initialised but later trained.

---

## 5. Recommended Open‑Source LLM

**Primary candidate: Llama‑3‑8B (Meta)**  
*Why:*

- Best‑in‑class performance for size among openly available LLMs (MMLU, reasoning).
- Strong community support, extensive adapter libraries (HuggingFace `transformers`, PEFT).
- 8B fits on a single 48GB GPU with full fine‑tuning using activation checkpointing.
- The 8k context length is generous for our tokenised flows.

**Fallback (for resource‑constrained settings): Phi‑3‑mini‑4k‑instruct (3.8B)**  
- Competitive with Llama‑3‑8B on many benchmarks, smaller memory footprint, good instruction‑following – useful if we later want to query the model for explanations.

**DeepSeek‑V2‑Lite (16B MoE, but 2.4B active) is another strong choice** because of its massive pretrained corpus and MoE efficiency, but community adoption and tooling are slightly less mature.

I will use **Llama‑3‑8B** as the reference backbone.

---

## 6. Complete Spectre Architecture

Spectre mirrors Garak’s design philosophy: **probes**, **harness**, **evaluators**, and **reporting**. However, instead of text prompts, it manipulates `.pcap` files, the tokenisation pipeline, and the model’s feature representation.

### System Components

```
Spectre Framework
├── Core
│   ├── Probe Registry (plugin system)
│   ├── Harness (orchestrates runs)
│   ├── Mutation Engine (packet-level transformations)
│   ├── Config Management (YAML/JSON profiles)
│   └── Logging & Persistence
├── Target Model Interface
│   ├── Classifier Wrapper (loads model, tokeniser, preprocessor)
│   └── Inference API (predict, predict_proba)
├── Attack Families (Plugins)
│   ├── Evasion (Phase 1)
│   ├── Confidence Manipulation
│   ├── Parser Attacks
│   ├── Prompt Attacks (if text-based variant)
│   ├── Representation Attacks (attack VQ codebook or tokenisation)
│   ├── Feature Perturbation
│   └── Flow Mutation
├── Evaluators
│   ├── Evasion Success Rate
│   ├── Confidence Shift
│   ├── Fidelity Metrics (functional preservation)
│   ├── Resource Overhead (bandwidth, latency)
│   └── Decision Boundary Analysis
└── Reporting
    ├── HTML/JSON Reports
    ├── Dashboard (optional)
    └── Dataset Export (adversarial pcaps + labels)
```

The **Probe Registry** uses a Python entry‑points mechanism: each attack family provides a directory with probe classes inheriting from `BaseProbe`. The harness discovers them dynamically.

### Plug-In Example (Evasion)

`probes/evasion/tcp_timing.py`:
- Class `TCPTimingJitter` inherits from `EvasionProbe`.
- Implements `generate(pcap_path) → Iterable[AdversarialSample]`.
- Uses Scapy to shift inter‑packet delays by a random ±ε, respecting flow boundaries.

All probes are stateless and accept a configuration dict.

---

## 7. Modular Attack/Probe Hierarchy

Attack families are top‑level categories. Within each, multiple **probe groups** exist, and each group can contain several **specific probes** (variations of an attack).

```
Attack Family: Evasion
├── Timing Perturbation
│   ├── Uniform jitter
│   ├── Gaussian jitter
│   ├── Bounded IAT expansion
│   └── Chaff packets (insertion of empty packets)
├── Packet Padding
│   ├── Constant padding (N bytes)
│   ├── Random padding (uniform)
│   ├── Protocol‑compliant padding (e.g., TLS padding extension)
│   └── MTU‑targeted fragmentation
├── Fragmentation & Reordering
│   ├── IP fragmentation (8‑byte offset)
│   ├── TCP segmentation
│   ├── Packet reordering within window
│   └── Retransmission injection
├── Protocol Header Manipulation
│   ├── TCP option reordering/insertion
│   ├── TTL randomisation
│   ├── DNS case/compression tricks
│   ├── HTTP header order shuffling
│   └── TLS cipher suite reordering
├── Feature Masking
│   ├── Payload encryption mimicry (append AES‑like block)
│   ├── Entropy obfuscation
│   └── Flow duration elongation
└── Hybrid (combined probes)
    ├── Timing + Padding
    └── Fragmentation + Header Manipulation
```

Each probe is required to **preserve the functional semantics** of the traffic. The framework verifies this through a fidelity checker (e.g., replaying the mutated pcap in a sandbox and checking if the malware’s C2 communication still succeeds – simulated using a proxy).

---

## 8. Detailed Design for Evasion Attacks (Phase 1 Implementation)

### Mutation Engine

A standalone, reusable module that accepts a `Flow` object (a parsed, sequence‑aware representation of a bidirectional flow) and returns mutated flows.

Core classes:

- `FlowMutator`: abstract base.
- `TimingMutator`: modifies IATs; respects minimum inter‑packet gap to avoid merging packets.
- `PaddingMutator`: inserts or enlarges payload data; updates IP total length/TCP sequence numbers.
- `FragmentMutator`: splits IP datagrams; handles reassembly in tests.
- `HeaderMutator`: rewrites TCP options, TTL, etc., using precise template rules.

The engine leverages Scapy for packet crafting and PcapWriter for output.

### Probe Example: Uniform Jitter

1. Input: pcap with malware flow.
2. Parse flow, extract timing array.
3. For each inter‑packet gap, add a random value from `[-max_jitter, max_jitter]` (clipped at 1 ms minimum to avoid zero/negative).
4. Rebuild pcap with updated timestamps, preserving all other packet contents.
5. Return adversarial pcap + metadata (probe name, parameters, fidelity check result).

### Evaluation Pipeline

1. **Baseline**: Classify original pcap → label “malware”, confidence 0.97.
2. **Attack**: For each probe and parameter set, generate N variants.
3. **Classification**: Run target model; record new label and confidence.
4. **Fidelity**: If sandbox confirms malicious intent, mark as valid adversarial sample.
5. **Metrics** (see Section 11).

---

## 9. Evaluation Methodology

- **Dataset Split**: 70/15/15 train/validation/test. The test set is held back from any model training and probe development. An independent “adversarial test set” is curated from new captures not used in probe design.
- **Attack Strength Parameters**: Each probe is evaluated over a grid of parameter values to produce robustness curves (e.g., jitter range vs. evasion rate).
- **Threat Models**:
  - *Black‑box*: Attacker only knows the API, can submit pcaps and observe labels.
  - *Grey‑box*: Attacker knows the feature extraction pipeline (but not model weights), used for representation attacks.
  - *White‑box*: Full access to model gradients (used later for adversarial optimisation probes).
- **Baselines**: Compare the LLM classifier against traditional ML (XGBoost on flow stats, 1D‑CNN on raw packet bytes, LSTM on packet‑level features) under the same attacks to quantify added robustness or fragility.
- **Significance Testing**: McNemar’s test, paired bootstrap confidence intervals for success rates.

---

## 10. Benchmark Design

The Spectre benchmark consists of:

1. **Curated Clean Dataset**: ~50,000 labelled flows (benign + diverse malware families) with ground‑truth PCAPs.
2. **Adversarial Corpus**: For each probe and parameter set, a set of mutated pcaps with fidelity verification logs.
3. **Reference Classifier**: Our LLM‑based model (trained weights publicly released).
4. **Evaluation Harness**: Spectre framework itself as the benchmarking tool.
5. **Leaderboard Metrics**: Overall Robustness Score (Section 11), per‑family breakdown, and attack‑transferability matrix.

All data is versioned and released under a research‑friendly license.

---

## 11. Metrics

**Primary**

- **Evasion Success Rate (ESR)**: Fraction of malware flows that become classified as benign after perturbation, under the fidelity constraint.
- **Confidence Drop (CD)**: Average decrease in malicious class confidence for successfully evaded samples.

**Secondary**

- **Fidelity Failure Rate**: Proportion of perturbed samples that no longer exhibit malware functionality (should be low; a probe is valid only if this remains small).
- **Overhead Factor**: Ratio of bytes (or duration) in adversarial pcap vs. original; measures how “expensive” evasion is.
- **Detection AUC under Attack**: The ROC‑AUC of the classifier on a balanced set of clean benign + adversarial malware flows.

**Proposed Spectre Robustness Score**  
`S = (1 – ESR) × (1 – CD_mean)`  
Normalised such that a perfect classifier gets 1.0, a completely broken one gets 0.0.

---

## 12. Recommended Software Architecture

- **Language**: Python 3.11+
- **Packet Manipulation**: Scapy 2.5+, PcapPlusPlus Python bindings for speed
- **Feature Extraction**: nfstream, custom Cython modules for per‑packet parsing
- **Model Training & Inference**: PyTorch 2.2+, HuggingFace `transformers`, PEFT, DeepSpeed
- **Vector Quantization**: `vector-quantize-pytorch` or custom VQ layer
- **Orchestration**: Hydra for config, DVC for data versioning, MLflow for tracking
- **Probe Plugin System**: `importlib.metadata` entry points, each probe a class
- **Evaluation Backend**: Custom, using multiprocessing to parallelize pcap mutation and classification
- **Reporting**: Jinja2 templates → static HTML + JSON

Containerized deployment with Docker; GPU support via nvidia-docker.

---

## 13. Folder Structure

```
spectre/
├── README.md
├── pyproject.toml
├── configs/                    # Hydra YAML files per experiment
├── data/
│   ├── raw/                    # original pcap, labels
│   ├── processed/              # tokenised flows, train/val/test splits
│   └── adversarial/            # generated adversarial pcaps
├── src/
│   ├── classifier/             # model definition, training scripts, tokenizer
│   │   ├── traffic_tokenizer.py
│   │   ├── vq_encoder.py
│   │   ├── llama_model.py
│   │   └── train.py
│   ├── spectre/
│   │   ├── core/
│   │   │   ├── harness.py
│   │   │   ├── probe_registry.py
│   │   │   └── mutation_engine.py
│   │   ├── probes/
│   │   │   ├── base.py
│   │   │   ├── evasion/
│   │   │   │   ├── timing.py
│   │   │   │   ├── padding.py
│   │   │   │   ├── fragmentation.py
│   │   │   │   ├── header_manip.py
│   │   │   │   └── feature_masking.py
│   │   │   └── future/         # confidence, parser, etc.
│   │   ├── evaluators/
│   │   │   ├── metrics.py
│   │   │   └── fidelity_checker.py
│   │   └── reporting/
│   │       ├── templates/
│   │       └── generate_report.py
│   └── utils/
│       ├── pcap_utils.py
│       └── flow_parser.py
├── tests/                      # unit & integration tests
├── scripts/                    # data preparation, benchmark runs
└── docs/
    └── design.md
```

---

## 14. Development Milestones

| Milestone | Deliverable | Timeline |
|-----------|-------------|----------|
| M1: Data Pipeline | Extract flows, train VQ tokenizer, build tokenised dataset | Month 1 |
| M2: Baseline Classifier | Train LLM classifier (full FT), achieve >95% F1 on test | Month 2–3 |
| M3: Spectre Core | Implement harness, probe registry, basic mutation engine (timing, padding) | Month 4 |
| M4: First Evasion Probes | 5 probes fully functional with fidelity checks | Month 5 |
| M5: Evaluation & Benchmark | Run all probes against classifier, generate benchmark data and report | Month 6–7 |
| M6: Write‑up & Release | Paper draft, open‑source code, dataset | Month 8 |

---

## 15. Potential Research Contributions

1. **Tokenised Traffic Representation for LLMs**  
   A novel method to convert network flows into a language model‑compatible discrete sequence, enabling LLM‑based traffic classification without catastrophic token bloat.

2. **First Comprehensive Robustness Benchmark for LLM‑Based Traffic Classifiers**  
   Systematic evaluation under multiple evasion strategies, revealing failure modes invisible to traditional ML baselines.

3. **Modular Adversarial Framework (Spectre)**  
   Inspired by Garak but specifically designed for the network domain, with a reusable mutation engine and fidelity‑aware probe hierarchy.

4. **Empirical Discovery of Fragile Dependencies**  
   We expect LLMs to over‑rely on high‑level timing patterns or specific header fields; Spectre will quantify this and suggest defenses.

5. **Guidance for Secure Deployment**  
   Recommendations on how to harden such classifiers, possibly through adversarial training with Spectre‑generated traffic.

---

## 16. Risks and Mitigation

| Risk | Mitigation |
|------|------------|
| Tokenised representation loses subtle discriminative features | Ablate by comparing with raw‑packet‑byte CNN; iterate on feature set. |
| Full fine‑tuning of 8B model exceeds GPU budget | Fallback to QLoRA + a smaller model; accept small accuracy drop. |
| Fidelity checking is imperfect (malware sandbox not 100% reliable) | Use multiple sandboxes, manual review on a sample, report fidelity failure bounds. |
| Probe‑generated traffic breaks flow parsing | Implement robust fallback: if flow extraction fails, skip sample and log. |
| Dataset licensing / privacy | Use only publicly available malware pcaps (CTU‑13, CIC‑IDS, etc.) with appropriate anonymisation. |

---

## 17. Future Extensions

- **Defensive probes**: Evaluate adversarial training, input preprocessing, ensemble methods.
- **Prompt attacks**: If the classifier is later exposed through an LLM‑based security analyst assistant, explore how natural language prompts can mislead the system.
- **Transfer attacks**: Train surrogate models to create black‑box evasion traffic that transfers to the LLM.
- **Real‑time evasion**: Stream‑based attacks that inject adversarial packets live.
- **Explainability analysis**: Use the LLM to generate natural language explanations for its classifications, then attack those explanations.

---

## 18. Prioritized Implementation Plan (MVP → Publication)

**MVP (Minimum Viable Product)**
1. Implement `traffic_tokenizer.py` and VQ training on a subset of data.
2. Fine‑tune Llama‑3‑8B on tokenised flows for binary classification (malware/benign).
3. Build `mutation_engine.py` with two probe categories: `uniform_jitter` and `random_padding`.
4. Create `harness.py` that runs classifier on original + adversarial pcaps, computes ESR.
5. Package as a runnable script with a simple JSON report.

**Beyond MVP → Spectre v0.1**
- Add remaining evasion probes.
- Implement fidelity checker (basic proxy replay).
- Build plugin system with entry points.
- Produce adversarial dataset and benchmark.
- Write paper.

---

## 19. Research Gap Analysis (Critical Assessment)

**Existing work**
- *LLMs for network traffic classification*: Most attempts feed Wireshark text summaries or Zeek logs to an LLM (e.g., “NetGPT”, “FlowLens”). These are token‑inefficient and have never been systematically evaluated for robustness. No work uses a learned discrete tokenisation of packet sequences for LLMs.
- *Adversarial ML for network intrusion/malware detection*: Rich literature on evasion for traditional ML (e.g., PDF malware, Android, PCAP attacks). The attacks manipulate feature vectors directly; no framework targets LLM‑specific representations.
- *Garak*: Holistic LLM vulnerability scanner but purely for text‑based NLP tasks (prompt injection, encoding, etc.). Does not touch network data or physical packet manipulation.
- *Network traffic benchmarks*: UNSW‑NB15, CIC‑IDS‑2017, CTU‑13 lack adversarial components; none test LLM classifiers.

**Underexplored areas Spectre fills**
1. **Discrete tokenisation of packet streams as a new input modality for LLMs**, bridging the gap between network security and foundation models.
2. **Adversarial robustness of LLM-based traffic classifiers** – completely open. No published work examines how packet‑level mutations affect these models.
3. **Fidelity‑aware adversarial traffic generation** – ensuring malware functionality post‑perturbation is non‑trivial and largely ignored in prior evasion research that changes statistical features without regard to protocol semantics.
4. **Modular, extensible benchmark framework** specifically for traffic analysis models, analogous to Garak’s role for LLM safety.

**Novelty critique**  
Simply applying existing evasion attacks to a new model is incremental. The genuine innovation is the **end‑to‑end design**:

- The tokenised flow representation → makes LLM applicable to raw traffic.
- The Spectre probe hierarchy tailored to network protocol layers.
- The fidelity‑constrained evaluation (most existing evasion papers ignore whether the perturbed malware still works, focusing only on classifier output).
- The integration of LLM‑specific vulnerabilities (e.g., representation attacks targeting the VQ codebook, prompt attacks if the classifier has a text interface) – these are entirely new threat surfaces.

Thus, the project is positioned to make a **strong, multi‑contribution submission** to IEEE S&P, USENIX Security, or NDSS.

---

## Final Thoughts

Spectre is designed as a long‑term research instrument. The initial focus on a high‑accuracy LLM‑based classifier and a disciplined evasion attack suite will yield immediate insights, while the modular architecture ensures the project can grow into the definitive benchmark for traffic analysis robustness. The fusion of discrete traffic tokenisation with LLM fine‑tuning addresses a real and unexplored gap, and the adversarial evaluation methodology goes beyond “just another evasion paper” by introducing fidelity constraints and a principled probe hierarchy.

This blueprint should serve as the foundation for a compelling, publication‑ready research effort.

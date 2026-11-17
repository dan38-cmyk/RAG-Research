# Data analyst learning assistant

#### Scope and research question

The learner approved the AI-proposed **data analyst learning assistant** topic. The following technical plan is AI-drafted for review, not a built application or independently explained learner architecture.

- Reader: a beginner studying SQL and pandas for data analyst work.
- Problem hypothesis: beginners need help locating relevant official explanations and distinguishing SQL operations from pandas operations. No user research has yet established frequency or demand.
- Research question: can a small, versioned collection of official tutorials support useful beginner answers with inspectable supporting passages and honest handling of missing evidence?
- Proposed scope: explain selecting/filtering, aggregation and combining tables, with source links. No employer data, arbitrary uploads, execution of user code, career promises or unrestricted web search.

#### Research-review index and original sources

Sources were opened by AI during this planning chat. Source facts below are distinct from design proposals. Learner verification and peer review remain pending.

| Source | Finding / use |
|---|---|
| [PostgreSQL tutorial](https://www.postgresql.org/docs/18/tutorial.html) | Beginner SQL source collection; pin the major version rather than silently follow a changing current alias. |
| [PostgreSQL license](https://www.postgresql.org/about/licence/) | Explicitly permits reuse of software and documentation subject to retaining its notices. Preserve notices with imported copies. |
| [pandas introductory tutorials](https://pandas.pydata.org/docs/getting_started/intro_tutorials/) | Candidate material for table selection, summary statistics and combining tables. Record the actual version and retrieval date when importing. |
| [pandas project license](https://github.com/pandas-dev/pandas/blob/main/LICENSE) | BSD 3-Clause terms; retain applicable notices and disclaimers. Confirm selected documentation files and bundled examples have no additional notices before import; exclude separately licensed linked datasets/images. |
| [RAG research paper, Lewis et al.](https://arxiv.org/abs/2005.11401) | Describes combining a retriever and a generator. Retrieval supplies evidence; it does not guarantee correct generated claims. |
| [Sentence Transformers semantic search](https://sbert.net/examples/sentence_transformer/applications/semantic-search/README.html) | Documents embedding queries/passages into a common vector space and ranking similar passages. Model suitability for short questions versus longer passages matters. |
| [pgvector](https://github.com/pgvector/pgvector) | Documents vector similarity search in PostgreSQL. Candidate vector storage without a separate vector database service. |
| [Neo4j graph concepts](https://neo4j.com/docs/getting-started/appendix/graphdb-concepts/) | Nodes and relationships provide an explicit graph representation; useful for comparing a concept/dependency graph alternative. |
| [PostgreSQL full-text search](https://www.postgresql.org/docs/current/textsearch.html) | Keyword retrieval baseline to compare with semantic retrieval before claiming improvement. |

#### Compare before choosing

| Approach | Proposed representation / retrieval | Benefit for this problem | Cost / limitation |
|---|---|---|---|
| Vector RAG | Embed documentation passages and questions; rank by similarity and filter by tool/version. | May retrieve explanations when a beginner uses different words from the documentation. | Similarity can return the wrong operation or tool; requires model choice, evaluation and source inspection. |
| Graph RAG | Nodes for tools, operations, pages and versions; edges such as DOCUMENTS, BELONGS_TO and REQUIRES; retrieve via explicit relationships. | Makes dependencies and multi-step concept relationships inspectable. | Requires a verified schema, entity extraction and relationship maintenance; a graph alone does not solve paraphrase matching. |

AI-recommended initial decision: **vector RAG**, with PostgreSQL/pgvector proposed for metadata and vectors and a keyword baseline for evaluation. The initial questions concern explanations in passages, rather than multi-hop relationships. Do not add a separate graph service until an evaluation need justifies it. Graph databases can also support vector indexes; this comparison is about proposed representations, not mutually exclusive product capabilities. Learner reviewed the draft and said it looked good; no independent explanation of this recommendation is claimed.

#### Proposed import, representation and architecture

1. Maintain a small allowlist (initial cap: 20 tutorial pages). Check licenses/notices, URLs and versions; fetch at a low rate and cache permitted copies. Exclude private, login-only and unrelated linked content.
2. Extract main text, headings and code examples, removing menus. Split at headings into passages with a provisional 300–600-token target and limited overlap. Keep code/explanations together when practical. Chunking trades retrieval focus against missing context; inspect examples and adjust rather than treating these numbers as proven.
3. Store source URL, title, heading anchor, version, fetch date, license reference, content hash and stable chunk ID. Upsert by source/version/hash so repeat import does not duplicate content. Report empty/failed imports instead of silently indexing them.
4. Embed chunks using one pinned, license-checked sentence embedding model. An embedding is a numeric representation used for similarity, not a guarantee of truth. Store the model identifier/dimension with vectors; re-embed when the model changes.
5. A proposed separate FastAPI RAG application accepts a bounded question and SQL/pandas selection, embeds the query using the same model and retrieves up to four matching passages. No changes to the working portfolio or its account database are authorized by this plan.
6. Supply only retrieved evidence to a selected text-generation model, requesting a concise answer with chunk-linked citations. Evidence is data, not instructions. If retrieval is inadequate, report insufficient evidence. Similarity alone cannot prove support; validate answer support in evaluation. Show cited passages so a reader can inspect them.
7. Generation/embedding model identifiers, licenses, memory use and hosting route are decision gates before Build. No API key, purchase, provider account, dependency installation or deployment is needed for Plan. An excerpt-only search prototype may validate retrieval, but must be labeled as such and is not a finished generative RAG app.

#### One proposed source-to-answer trace

Source: [PostgreSQL 18 aggregate tutorial](https://www.postgresql.org/docs/18/tutorial-agg.html). It explains grouping and the distinction between WHERE and HAVING. Import its main text and examples; attach its URL/heading/version to a chunk; embed and store that chunk. For “How do I filter groups after calculating totals?”, retrieve the aggregate passage. The proposed answer explains HAVING with a link to that exact evidence. A reviewer checks whether the passage actually supports the answer and whether the system accidentally recommends WHERE for the aggregate condition. This is a manually designed trace, **not an executed retrieval or generation result**.

#### Evaluation questions and five observable stories · all planned

| Story / input | Expected observable behavior | Defect it could expose |
|---|---|---|
| 1. Beginner asks “How do I filter groups after calculating totals?” with SQL selected | Aggregate/HAVING evidence appears in top four; answer distinguishes row filtering from group filtering and cites the source. | Missed paraphrase, unsupported answer or WHERE/HAVING confusion. |
| 2. Beginner asks “How do I calculate the average for each category?” with pandas selected | Retrieve supporting [pandas summary statistics](https://pandas.pydata.org/docs/getting_started/intro_tutorials/06_calculate_statistics.html) passages; explain groupby/mean with a supporting citation rather than SQL syntax. | Wrong-tool retrieval or code with no source support. |
| 3. Reader asks “What was Amazon's internal DEA target last week?” | State the approved collection does not contain that information; invent no target or citation. | Hallucinated private or out-of-scope facts. |
| 4. Maintainer imports an unchanged allowlisted source twice | Same chunk count/identifiers; source/version/license metadata remains intact; failures are visible. | Duplicate or untraceable imported evidence. |
| 5. Reader opens an answer and its citation on desktop/narrow view | Question, answer and cited passages remain usable; citation resolves to the recorded source section; model timeout produces a clear retry/error state. | Broken evidence links, unusable layout or hidden failures. |

Proposed evaluation: keep a versioned question set with expected supporting sections and assess retrieval separately from generation. Record retrieved IDs/ranks, answer claims/citations and actual latency for each run. Compare keyword and vector results on the same questions; inspect every initial answer for evidence support. Initial acceptance: both in-scope questions retrieve the correct supporting passage in the top four, every substantive answer claim has supporting evidence, the unsupported question abstains, and import/citation/UI stories pass. This small suite cannot establish general accuracy. No success rate, speed advantage or passed test is claimed.

#### Hosting and resources · unverified planning constraints

- Local development first; no hosted RAG URL exists. Hosting will be a separate agreed step through Server Studio, without changing this repository's deployment/proxy configuration.
- Start with at most 20 pages, capped imports/question/context sizes and cached offline embeddings. Avoid GPU assumptions and unbounded crawls.
- Before choosing models, inspect available RAM/CPU/disk, PostgreSQL/pgvector support, model-download sizes, CPU latency and license terms. A local generator may exceed the host's resources; hosted inference has privacy, network and cost constraints requiring a separate decision. No costs or capacity are verified.
- Proposed initial generation timeout: 30 seconds with a visible failure state; this is an engineering limit to evaluate, not measured performance.

- Peer review: Pending. Ask a peer to follow the aggregate-source trace, identify one unsupported assumption/tradeoff and explain how an evaluation question would reveal missing/incorrect evidence. Record actual feedback, decision and changed documentation here.
- Changed: learner selected the data analyst learning assistant topic; AI drafted source research, alternatives, proposed architecture, trace and evaluation stories.
- Checked: AI opened the linked original documentation, licenses and research. The aggregate and pandas pages contain relevant example material. No corpus was imported, models installed, retrieval executed, answer generated by the proposed app or hosting tested. A documentation trace is not a test run.
- Review: learner reported the draft looked good and authorized publication for peer review. Source reading by AI is distinguished from independent learner verification and executed tests.
- Next: obtain actual peer feedback and record the response; resolve model/hosting gates before implementation. Publication of this plan does not establish a hosted RAG app.

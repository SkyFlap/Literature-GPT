# Copyright 2024 the Literature-GPT team.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import TYPE_CHECKING, Dict, Tuple
import numpy as np
import heapq


def calc_cos_sim(emb_a, emb_b):
    sim = 0.0
    emb_a_np = np.array(emb_a)
    emb_b_np = np.array(emb_b)
    base = np.linalg.norm(emb_a_np) * np.linalg.norm(emb_b_np)
    if base != 0.0:
        sim = np.dot(emb_a_np, emb_b_np) / base
    return sim


def hybrid_search(
    query_embedding_vector: list[int], db_embedding_vectors: list[list[int]], n: int
) -> list[int]:
    sim_list = []
    for db_embedding_vector in db_embedding_vectors:
        sim_list.append(
            (calc_cos_sim(query_embedding_vector, db_embedding_vector), len(sim_list))
        )
    largest_n = heapq.nlargest(n, sim_list, key=lambda x: x[0])
    top_n_indices = [index for _, index in largest_n]
    return top_n_indices

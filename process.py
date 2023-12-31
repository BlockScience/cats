import pickle
from typing import Dict
import numpy as np
import ray


def function_0(batch: Dict[str, np.ndarray]) -> Dict[str, np.ndarray]:
    vec_a = batch["petal length (cm)"]
    vec_b = batch["petal width (cm)"]
    batch["petal area (cm^2)"] = vec_a * vec_b
    return batch

def function_1(batch: Dict[str, np.ndarray]) -> Dict[str, np.ndarray]:
    vec_a = batch["petal length (cm)"]
    vec_b = batch["petal width (cm)"]
    batch["DUPLICATE petal area (cm^2)"] = vec_a * vec_b
    return batch


def process_0(input, output):
    ds_in = ray.data.read_csv(input)
    ds_out = ds_in.map_batches(function_0)
    print(ds_out.show(limit=1))
    ds_out.write_csv(output)
    ray.shutdown()
    return ds_out

def process_1(input, output):
    ds_in = ray.data.read_csv(input)
    ds_out = ds_in.map_batches(function_1)
    print(ds_out.show(limit=1))
    ds_out.write_csv(output)
    ray.shutdown()
    return ds_out

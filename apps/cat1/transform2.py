def transform(cad):
    return cad.catContext['cao'] \
        .groupBy("row_sum_sum") \
        .sum("_c0_sum") \
        .show(truncate=False)

# transform = f
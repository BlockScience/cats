import json, glob, os, multiprocessing, shutil, subprocess, tempfile, time

# checkStatusOfJob checks the status of a Bacalhau job
def checkStatusOfJob(job_id: str) -> str:
    assert len(job_id) > 0
    p = subprocess.run(
        ["bacalhau", "list", "--output", "json", "--id-filter", job_id],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    r = parseJobStatus(p.stdout)
    if r == "":
        print("job status is empty! %s" % job_id)
    elif r == "Completed":
        print("job completed: %s" % job_id)
    else:
        print("job not completed: %s - %s" % (job_id, r))

    return r


# submitJob submits a job to the Bacalhau network
def submitJob(cid: str) -> str:
    assert len(cid) > 0
    p = subprocess.run(
        [
            "bacalhau",
            "docker",
            "run",
            "--id-only",
            "--wait=false",
            "--input",
            "ipfs://" + cid + ":/inputs/data.tar.gz",
            "ghcr.io/bacalhau-project/examples/blockchain-etl:0.0.6",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if p.returncode != 0:
        print("failed (%d) job: %s" % (p.returncode, p.stdout))
    job_id = p.stdout.strip()
    print("job submitted: %s" % job_id)

    return job_id


# getResultsFromJob gets the results from a Bacalhau job
def getResultsFromJob(job_id: str) -> str:
    assert len(job_id) > 0
    temp_dir = tempfile.mkdtemp()
    print("getting results for job: %s" % job_id)
    for i in range(0, 5): # try 5 times
        p = subprocess.run(
            [
                "bacalhau",
                "get",
                "--output-dir",
                temp_dir,
                job_id,
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        if p.returncode == 0:
            break
        else:
            print("failed (exit %d) to get job: %s" % (p.returncode, p.stdout))

    return temp_dir


# parseJobStatus parses the status of a Bacalhau job
def parseJobStatus(result: str) -> str:
    if len(result) == 0:
        return ""
    r = json.loads(result)
    if len(r) > 0:
        return r[0]["State"]["State"]
    return ""


# parseHashes splits lines from a text file into a list
def parseHashes(filename: str) -> list:
    assert os.path.exists(filename)
    with open(filename, "r") as f:
        hashes = f.read().splitlines()
    return hashes


def main(file: str, num_files: int = -1):
    # Use multiprocessing to work in parallel
    count = multiprocessing.cpu_count()
    with multiprocessing.Pool(processes=count) as pool:
        hashes = parseHashes(file)[:num_files]
        print("submitting %d jobs" % len(hashes))
        job_ids = pool.map(submitJob, hashes)
        assert len(job_ids) == len(hashes)

        print("waiting for jobs to complete...")
        while True:
            job_statuses = pool.map(checkStatusOfJob, job_ids)
            total_finished = sum(map(lambda x: x == "Completed", job_statuses))
            if total_finished >= len(job_ids):
                break
            print("%d/%d jobs completed" % (total_finished, len(job_ids)))
            time.sleep(2)

        print("all jobs completed, saving results...")
        results = pool.map(getResultsFromJob, job_ids)
        print("finished saving results")

        # Do something with the results
        shutil.rmtree("../../results", ignore_errors=True)
        os.makedirs("../../results", exist_ok=True)
        for r in results:
            path = os.path.join(r, "outputs", "*.csv")
            csv_file = glob.glob(path)
            for f in csv_file:
                print("moving %s to results" % f)
                shutil.move(f, "../../results")

if __name__ == "__main__":
    main("../../hashes.txt", 10)

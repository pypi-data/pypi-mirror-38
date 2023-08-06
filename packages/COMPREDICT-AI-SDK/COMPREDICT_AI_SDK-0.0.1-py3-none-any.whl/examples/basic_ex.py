from compredict.client import api
from compredict.resources import resources
from time import sleep
from environs import Env
from sys import exit


env = Env()
env.read_env()

token = env("COMPREDICT_AI_CORE_KEY")
callback_url = env("COMPREDICT_AI_CORE_CALLBACK", None)
fail_on_error = env("COMPREDICT_AI_CORE_FAIL_ON_ERROR", False)
ppk = env("COMPREDICT_AI_CORE_PPK", None)
passphrase = env("COMPREDICT_AI_CORE_PASSPHRASE", "")

client = api.get_instance(token=token, callback_url=callback_url, ppk=ppk, passphrase=passphrase)
client.fail_on_error(option=fail_on_error)
algorithms = client.get_algorithms()

# Check if the user has algorithms to predict
if len(algorithms) == 0:
    print("No algorithms to proceed!")
    exit()

algorithm = algorithms[0]

tmp = algorithm.get_detailed_template()
tmp.close()  # It is tmp file. close the file to remove it.

data = dict()  # data for predictions

results = algorithm.run(data, evaluate=False, encrypt=True)

if isinstance(results, resources.Task):
    print(results.job_id)

    while results.status != results.STATUS_FINISHED:
        print("task is not done yet.. waiting...")
        sleep(15)
        results.update()

    if results.success is True:
        print(results.predictions)
    else:
        print(results.error)

else:
    print(results.predictions)



import datetime
from dateutil import parser as dtparser
from biothings import config
logger = config.logger


# This will add a new console command "auto_archive".
# It is a private command only accessible from the ssh console
def auto_archive(build_config_name, days=3, dryrun=True):
    """
    Archive any builds which build date is older than today's date
    by "days" day.
    """
    logger.info("Auto-archive builds older than %s days" % days)
    builds = lsmerge(build_config_name)
    today = datetime.datetime.now().astimezone()
    at_least_one = False
    for bid in builds:
        build = bm.build_info(bid)
        try:
            bdate = dtparser.parse(build["_meta"]["build_date"]).astimezone()
        except KeyError:
            logger.warning('Build "{}" missing "_meta" key.'.format(bid))
            continue
        deltadate = today - bdate
        if deltadate.days > days:
            logger.info("Archiving build %s (older than %s)" % (bid, deltadate))
            if dryrun:
                logger.info("This is a dryrun of \"archive(%s)\", no real changes were made.", bid)
            else:
                archive(bid)
            at_least_one = True
    if not at_least_one:
        logger.info("Nothing to archive")


# the following line set the schedule to run it regularly in the event loop
# multiple schedules can be added for different build configs
schedule("0 17 * * *", auto_archive, "covid19", dryrun=False)   # 5pm daily, 1am UTC
schedule("0 18 * * *", auto_archive, "litcovid", dryrun=False)  # 6pm daily, 2am UTC
schedule("0 18 * * *", auto_archive, "biorxiv", dryrun=False)   # 6pm daily, 2am UTC
schedule("0 18 * * *", auto_archive, "clinical_trials", dryrun=False)   # 6pm daily, 2am UTC
schedule("0 18 * * *", auto_archive, "pdb", dryrun=False)       # 6pm daily, 2am UTC
schedule("0 18 * * *", auto_archive, "figshare", dryrun=False)  # 6pm daily, 2am UTC
schedule("0 18 * * *", auto_archive, "protocolsio", dryrun=False)   # 6pm daily, 2am UTC
schedule("0 18 * * *", auto_archive, "dataverse", dryrun=False)   # 6pm daily, 2am UTC
schedule("0 18 * * *", auto_archive, "genomics_api", dryrun=False, days=90)   # 6pm daily, 2am UTC


# optionally, we can expose command as an API endpoint
# $ curl -XPUT localhost:19180/auto_archive/covid19
#   or with additional parameters:
# $ curl -XPUT -d '{"days":25, "dryrun": false}' localhost:19180/auto_archive/covid19
expose(
    endpoint_name="auto_archive",
    command_name="auto_archive",
    method="put"
)

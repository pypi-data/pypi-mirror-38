from powerline.segments import with_docstring
from powerline.theme import requires_segment_info


@requires_segment_info
def vcsh_repo(pl, segment_info):
    #pl.debug('running vcsh_repo')

    try:
        vcsh_repo = segment_info['environ']['VCSH_REPO_NAME']
    except KeyError:
        return None
    except Exception as e:
        pl.error(e)
        return None

    return [{'contents': 'V %s' % vcsh_repo, 'highlight_groups': ['vcsh_repo']}]

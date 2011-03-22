from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from zoo.models import *
from datetime import datetime

def user_or_none(user):
    if user.is_anonymous():
        return None
    else:
        return user


# GET /api/specs/#/active    Gets the current active spec associated with this versionid
def specs_active(request, version_id):
    obj = Spec.objects.get(version__versionid__exact = version_id, version__active = True)
    return {
        'id': obj.version.id,
        'name': obj.name,
        'summary': obj.summary,
        'spec': obj.spec,
        'votes': obj.version.versionid.votes(),
    }

# GET /api/specs/#/all       Gets all the versions associated with this versionid
# GET /api/specs/#/snippets  Gets the active snippets in all languages associated with a spec versionid
# GET /api/spec/#            Gets the info in a specific version of a spec

# GET /api/snippets/#/active Gets the current active snippet associated with this snippet versionid
# GET /api/snippets/#/all    Gets all versions associated with this versionid
# GET /api/snippet/#         Get the info in snippet
# GET /api/snippet/#/raw     Gets the raw text of a given snippet

# POST /api/new/snippet      Creates a new snippet associated with a spec versionid (optional versionid)
def get_or_new_versionid(versionid_id):
    if versionid_id is None:
        v = VersionID()
        v.save()
        return v
    else:
        return VersionID.get(id=int(versionid_id))
    
def new_version(user, versionid):
    return Version(
        timestamp = datetime.now(), 
        user = user_or_none(user),
        active = True, 
        versionid = versionid)

def new_snippet(request):
    spec_versionid = VersionID.objects.get(id=int(request.POST['spec_versionid']))
    versionid = get_or_new_versionid(request.POST.get('versionid'))

    version = new_version(user=request.user, versionid=versionid)
    snippet = Snippet(version=version, 
                      code=request.POST['code'], 
                      language=request.POST['language'],
                      versionid=versionid)
    version.save()
    snippet.save()
    return {
        'versionid': versionid.id,
        'version': version.id,
    }
    
    



# POST /api/new/spec         Creates a new spec (optional versionid)
def new_spec(request):
    versionid = get_or_new_versionid(request.POST.get('versionid'))

    # TODO leave inactive if user is untrusted
    version = new_version(user=request.user, versionid=versionid)

    spec = Spec(version=version, name=request.POST.get('name') or "unnamed", summary=request.POST.get('summary') or "", spec=request.POST.get('spec') or "")
    
    version.save()
    spec.save()

    return {
        'versionid': versionid.id,
        'version': version.id,
    }


# POST /api/vote             Vote on a versionid


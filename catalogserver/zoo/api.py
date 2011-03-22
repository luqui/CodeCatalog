from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from zoo.models import *
from datetime import datetime

def user_or_none(user):
    if user.is_anonymous():
        return None
    else:
        return user

def new_version(user, versionptr):
    return Version(
        timestamp = datetime.now(),
        user = user_or_none(user),
        active = True,
        versionptr = versionptr)

def get_or_new_versionptr(versionptr_id):
    if versionptr_id is None:
        v = VersionPtr()
        v.save()
        return v
    else:
        return VersionPtr.objects.get(id=int(versionptr_id))

def dump_spec(spec):
    return {
        'versionptr': spec.version.versionptr.id,
        'version': spec.version.id,
        'name': spec.name,
        'summary': spec.summary,
        'spec': spec.spec,
        'votes': spec.version.versionptr.votes(),
    }

def dump_snippet(snippet):
    return {
        'versionptr': snippet.version.versionptr.id,
        'version': snippet.version.id,
        'spec_versionptr': snippet.spec_versionptr.id,
        'language': snippet.language,
        'code': snippet.code,
        'votes': snippet.version.versionptr.votes(),
    }

def version_to_spec(version):
    return version.spec

def version_to_snippet(version):
    return version.snippet

def active_version(versionptr):
    return Version.objects.filter(versionptr__exact = versionptr, active = True).latest('timestamp')

def all_versions(versionptr):
    return Version.objects.filter(versionptr__exact = versionptr).all()

# GET /api/specs/#/active    Gets the current active spec associated with this versionptr
def specs_active(request, versionptr):
    return dump_spec(version_to_spec(active_version(versionptr)))

# GET /api/specs/#/all       Gets all the versions associated with this versionptr
def specs_all(request, versionptr):
    return map(lambda x: dump_spec(version_to_spec(x)), all_versions(versionptr))
    
# GET /api/specs/#/snippets  Gets the active snippets in all languages associated with a spec versionptr

def specs_snippets(request, versionptr):
    objs = Snippet.objects.filter(spec_versionptr = versionptr)
    return map(dump_snippet, objs)

# GET /api/spec/#            Gets the info in a specific version of a spec

def spec(request, version):
    obj = Spec.objects.get(version__exact = version)
    return dump_spec(obj)

# GET /api/snippets/#/active Gets the current active snippet associated with this snippet versionptr

def snippets_active(request, versionptr):
    return dump_snippet(version_to_snippet(active_version(versionptr)))

# GET /api/snippets/#/all    Gets all versions associated with this versionptr

def snippets_all(request, versionptr):
    return map(lambda x: dump_snippet(version_to_snippet(x)), all_versions(versionptr))

# GET /api/snippet/#         Get the info in snippet

def snippet(request, version):
    return dump_snippet(Snippet.objects.get(version__exact = version))

# POST /api/new/snippet      Creates a new snippet associated with a spec versionptr (optional versionptr)
    
def new_snippet(request):
    spec_versionptr = VersionPtr.objects.get(id=int(request.POST['spec_versionptr']))
    versionptr = get_or_new_versionptr(request.POST.get('versionptr'))

    version = new_version(user=request.user, versionptr=versionptr)
    version.save()
    snippet = Snippet(version=version, 
                      code=request.POST['code'], 
                      language=request.POST['language'],
                      spec_versionptr=spec_versionptr)
    snippet.save()
    return {
        'versionptr': versionptr.id,
        'version': version.id,
    }
    

# POST /api/new/spec         Creates a new spec (optional versionptr)
def new_spec(request):
    versionptr = get_or_new_versionptr(request.POST.get('versionptr'))

    # TODO leave inactive if user is untrusted
    version = new_version(request.user, versionptr)
    spec.save()

    spec = Spec(version=version, name=request.POST.get('name') or "unnamed", summary=request.POST.get('summary') or "", spec=request.POST.get('spec') or "")
    spec.save()

    return {
        'versionptr': versionptr.id,
        'version': version.id,
    }


# POST /api/vote             Vote on a versionptr

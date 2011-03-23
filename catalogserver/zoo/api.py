from zoo.models import *
from datetime import datetime

# Versions are organized into versionptrs, which essentially represents
# a collection of versions of the same thing.  When we view a spec or a
# snippet on the site, we refer to it using a versionptr, and we see
# the latest active version.
# Versions and versionptrs are separate, numeric namespaces. Versionptr 1
# and version 1 are not related.

def distinct_by(f, xs):
    cur = None
    for x in xs:
        fx = f(x)
        if cur != fx:
            cur = fx
            yield x

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
    """The representation of a spec.  This is what the methods that return a spec return."""
    return {
        'versionptr': spec.version.versionptr.id,
        'version': spec.version.id,
        'name': spec.name,
        'summary': spec.summary,
        'spec': spec.spec,
        'votes': spec.version.versionptr.votes,
        'timestamp': spec.version.timestamp.isoformat(),
    }

def dump_snippet(snippet):
    """The representation of a snippet.  This is what the methods that return a snippet return."""
    return {
        'versionptr': snippet.version.versionptr.id,
        'version': snippet.version.id,
        'spec_versionptr': snippet.spec_versionptr.id,
        'language': snippet.language,
        'code': snippet.code,
        'votes': snippet.version.versionptr.votes,
        'timestamp': snippet.version.timestamp.isoformat(),
    }

def version_to_spec(version):
    return version.spec

def version_to_snippet(version):
    return version.snippet

def active_version(versionptr):
    return Version.objects.filter(versionptr = versionptr, active = True).latest('timestamp')

def all_versions(versionptr):
    return Version.objects.filter(versionptr = versionptr).all()

def specs_active(request, versionptr):
    """GET /api/specs/<ptr>/active/ : Get the latest active spec with versionptr <ptr>."""
    return dump_spec(version_to_spec(active_version(versionptr)))

def specs_all(request, versionptr):
    """GET /api/specs/<ptr>/all/ : Get all spec versions associated with versionptr <ptr>."""
    return map(lambda x: dump_spec(version_to_spec(x)), all_versions(versionptr))
    
def specs_snippets(request, versionptr):
    """GET /api/specs/<ptr>/snippets/ : Get all snippets associated with the spec versionptr <ptr>."""
    objs = Snippet.objects.filter(spec_versionptr = versionptr)
    return map(dump_snippet, objs)

def specs_snippets_active(request, versionptr):
    """GET /api/specs/<ptr>/snippets/active/ : Gets the current active snippet in each language on the given spec versionptr"""
    objs = Snippet.objects.filter(spec_versionptr=versionptr, version__active=True).order_by('language', '-version__timestamp')
    return dict([ (snip.language, dump_snippet(snip)) 
                        for snip in distinct_by(lambda x: x.language, objs) ])

def spec(request, version):
    """GET /api/spec/<ver>/ : Get the spec at version <ver>."""
    return dump_spec(Spec.objects.get(version = version))

def snippets_active(request, versionptr):
    """GET /api/snippets/<ptr>/active/ : Gets the current active snippet associated with snippet versionptr <ptr>."""
    return dump_snippet(version_to_snippet(active_version(versionptr)))

def snippets_all(request, versionptr):
    """GET /api/snippets/<ptr>/all/ : Gets all versions of snippets associated with snippet versionptr <ptr>."""
    return map(lambda x: dump_snippet(version_to_snippet(x)), all_versions(versionptr))

def snippet(request, version):
    """GET /api/snippet/<ver>/ : Gets the snippet at version <ver>."""
    return dump_snippet(Snippet.objects.get(version = version))

def new_snippet(request):
    """POST /api/new/snippet/ : Creates a new snippet.

        spec_versionptr : what spec versionptr to associate this code with
        versionptr : (optional) what versionptr to make a new version of. 
                     Allocates new versionptr if not given.
        code : The code in the snippet
        language : The language the snippet is wirtten in
    """
    
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
    
def new_spec(request):
    """POST /api/new/spec/ : Creates a new spec.

        versionptr: (optional) what versionptr to add this version to.
                    Allocates new if not given.
        name: (optional) Name of this spec ("unnamed" if not given)
        summary: (optional) Summary of this spec ("" if not given)
        spec: (optinal) Description of this spec ("" if not given)
    """
    versionptr = get_or_new_versionptr(request.POST.get('versionptr'))

    # TODO leave inactive if user is untrusted
    version = new_version(request.user, versionptr)
    version.save()

    spec = Spec(version=version, name=request.POST.get('name') or "unnamed", summary=request.POST.get('summary') or "", spec=request.POST.get('spec') or "")
    spec.save()

    return {
        'versionptr': versionptr.id,
        'version': version.id,
    }

def vote(request):
    """POST /api/vote/ : Votes on a versionptr.  Cancels out any previous vote.

        versionptr: the versionptr to vote on
        value: -1, 0, or 1"""

    # TODO race condition
    versionptr = VersionPtr.objects.get(id=request.POST['versionptr'])
    value = int(request.POST['value'])
    
    pvotes = Vote.objects.filter(user=request.user, versionptr=versionptr)
    for pvote in pvotes:
        versionptr.votes -= pvote.value
    pvotes.delete()
    
    if value != 0:
        vote = Vote(user=request.user, versionptr=versionptr, value=value, date=datetime.now())
        versionptr.votes += value
        vote.save()
    versionptr.save()

    return ""

from zoo.models import *
from datetime import datetime
from haystack.query import SearchQuerySet
from django.db.models import Q
from django.contrib.auth import authenticate

# Versions are organized into versionptrs, which essentially represents
# a collection of versions of the same thing.  When we view a spec or a
# snippet on the site, we refer to it using a versionptr, and we see
# the latest active version.
# Versions and versionptrs are separate, numeric namespaces. Versionptr 1
# and version 1 are not related.


def login_required(f):
    def fprime(request, *args, **kwargs):
        if request.user.is_authenticated():
            return f(request, *args, **kwargs)
        else:
            post = request.POST
            if 'user' in post and 'api_key' in post:
                user = authenticate(username=request.POST['user'], password=request.POST['api_key'])
                if user is not None:
                    request.user = user
                    return f(request, *args, **kwargs)
                else:
                    return { 'error': 'Authentication failed' }
            else:
                return { 'error': 'Request requires authentication' }
    return fprime

def user_or_none(user):
    if user.is_anonymous():
        return None
    else:
        return user

def new_version(user, versionptr, comment=""):
    return Version(
        timestamp = datetime.now(),
        user = user_or_none(user),
        approved = True,
        active = True,
        versionptr = versionptr,
        comment = comment)

def get_or_new_versionptr(typ, versionptr_id):
    if versionptr_id is None:
        v = VersionPtr(type=VersionPtr.PTRTYPE_TO_ID[typ])
        v.save()
        return v
    else:
        return VersionPtr.objects.get(id=int(versionptr_id))

def update_active(versionptr):
    objs = Version.objects.filter(versionptr=versionptr)
    objs.update(active=False)
    activeobjs = objs.filter(approved=True).order_by('-timestamp')
    if activeobjs.exists():
        activeobj = activeobjs[0]
        activeobj.active=True
        activeobj.save()
    versionptr.save()

def notify_followers(user, versionptr):
    q = Q(followed=versionptr)
    if not user.is_anonymous(): 
        q = q & ~Q(follower=user)
    Following.objects.filter(q).update(new_events=True)

def latest_version(cls, versionptr):
    return cls.objects.filter(version__versionptr=versionptr).order_by('-version__timestamp')[0]

def get_versionptr_name(versionptr):
    typ = VersionPtr.ID_TO_PTRTYPE[versionptr.type]
    if typ == 'Spec':
        return latest_version(Spec, versionptr).name
    elif typ == 'Snippet':
        snip = latest_version(Snippet, versionptr)
        return get_versionptr_name(snip.spec_versionptr)
    elif typ == 'BugReport':
        return latest_version(BugReport, versionptr).title
    return "???"

def get_events_date_range(versionptr, startdate, enddate):
    versionptr_type = VersionPtr.ID_TO_PTRTYPE[versionptr.type]
    
    events = []
    name = get_versionptr_name(versionptr)
    for v in Version.objects.filter(versionptr=versionptr, timestamp__gt=startdate, timestamp__lt=enddate):
        events.append({
            'type': 'new_version',
            'versionptr': versionptr.id,
            'versionptr_type': versionptr_type,
            'version': v.id,
            'timestamp': v.timestamp.isoformat(),
            'name': name,
        })
    for bug in BugReport.objects.filter(target_versionptr=versionptr, version__timestamp__gt=startdate, version__timestamp__lt=enddate):
        events.append({
            'type': 'bug',
            'versionptr': versionptr.id,
            'versionptr_type': versionptr_type,
            'timestamp': bug.version.timestamp.isoformat(),
            'bug_version': bug.version.id,
            'bug_versionptr': bug.version.versionptr.id,
            'name': name,
            'bug_title': bug.title,
        })
    return events

def dump_spec(spec):
    """The representation of a spec.  This is what the methods that return a spec return."""
    return {
        'versionptr': spec.version.versionptr.id,
        'version': spec.version.id,
        'approved': spec.version.approved,
        'active': spec.version.active,
        'name': spec.name,
        'summary': spec.summary,
        'spec': spec.spec,
        'timestamp': spec.version.timestamp.isoformat(),
        'comment': spec.version.comment,
        'user': spec.version.user and spec.version.user.username,
        'status': Spec.ID_TO_STATUS[spec.status],
    }

def dump_snippet(snippet):
    """The representation of a snippet.  This is what the methods that return a snippet return."""
    return {
        'versionptr': snippet.version.versionptr.id,
        'version': snippet.version.id,
        'approved': snippet.version.approved,
        'active': snippet.version.active,
        'dependencies': tuple(snippet.dependency_set.all().values_list('target', flat=True)),
        'spec_versionptr': snippet.spec_versionptr.id,
        'language': snippet.language,
        'code': snippet.code,
        'timestamp': snippet.version.timestamp.isoformat(),
        'comment': snippet.version.comment,
        'user': snippet.version.user and snippet.version.user.username,
    }

def dump_bug(bug):
    return {
        'versionptr': bug.version.versionptr.id,
        'version': bug.version.id,
        'active': bug.version.active,
        'target_versionptr': bug.target_versionptr.id,
        'title': bug.title,
        'status': BugReport.ID_TO_STATUS[bug.status],
        'timestamp': bug.version.timestamp.isoformat(),
        'comment': bug.version.comment,
        'user': bug.version.user and bug.version.user.username,
    }

# CodeCatalog Snippet http://www.codecatalog.net/10/20/
def traverse_cons_list(conslist):
    while conslist is not ():
        (x,xs) = conslist
        yield x
        conslist = xs
# End CodeCatalog Snippet

# CodeCatalog Snippet http://www.codecatalog.net/12/186/
import heapq
# End CodeCatalog Snippet

# CodeCatalog Snippet http://www.codecatalog.net/14/32/
def shortest_path(children, success, init):
    seen = {}
    q = [(0, init, ())]
    if success(init):
        return ()
    while q:
        (weight, elem, tail) = heapq.heappop(q)
        if elem in seen: continue
        seen[elem] = 1

        for (cweight,child,edge) in children(elem):
            if success(child): return tuple(traverse_cons_list((edge,tail)))
            heapq.heappush(q, (weight+cweight,child, (edge,tail)))
    return None
# End CodeCatalog Snippet

# CodeCatalog Snippet http://www.codecatalog.net/146/390/
def uncons_set(s):
    clone = set(s)
    x = clone.pop()
    return (x, frozenset(clone))
# End CodeCatalog Snippet

# CodeCatalog Snippet http://www.codecatalog.net/148/414/
def dependency_search(members, type):
    def children(elem):
        (typ, rest) = uncons_set(elem)
        mems = list(members(typ))
        return (( mem.weight, mem.deps | rest, mem.object ) for mem in mems)
    def success(satset):
        return len(satset) == 0
    return shortest_path(children, success, frozenset((type,)))
# End CodeCatalog Snippet

from collections import namedtuple
AnnotatedMember = namedtuple('AnnotatedMember', ['weight', 'deps', 'object'])

def snippet_dependencies(snip):
    return frozenset(snip.dependency_set.values_list('target', flat=True))

def specs_assemble(request, versionptr):
    """GET /api/specs/<ptr>/assemble/ : Get a list of snippets which transitively assemble a spec"""
    def members(vptr):
        for o in Snippet.objects.filter(spec_versionptr=vptr, version__active=True):
            yield AnnotatedMember(
                    weight=0,
                    deps=snippet_dependencies(o),
                    object=o)
    return map(dump_snippet, dependency_search(members, versionptr) or ()) or None

def snippet_assemble(request, version):
    """GET /api/snippet/<version>/assemble/ : Get a list of snippets which transitively assemble,
       a spec, where the top level is a specific snippet.
    """
    snippet = Snippet.objects.get(version=int(version))
    
    def lang_members(vptr):
        for o in Snippet.objects.filter(
                    spec_versionptr=vptr, 
                    version__active=True,
                    language=snippet.language):
            yield AnnotatedMember(
                    weight=0,
                    deps=snippet_dependencies(o),
                    object=o)
    def members(vptr):
        def filt(o):
            return not o.object.spec_versionptr == snippet.spec_versionptr \
                   or o.object.version == snippet.version
        return filter(filt, lang_members(vptr))
    
    return map(dump_snippet, dependency_search(members, snippet.spec_versionptr) or ()) or None
    
def specs_active(request, versionptr):
    """GET /api/specs/<ptr>/active/ : Get the latest active spec with versionptr <ptr>."""
    return dump_spec(Spec.objects.get(version__versionptr=versionptr, version__active=True))

def specs_all(request, versionptr):
    """GET /api/specs/<ptr>/all/ : Get all spec versions associated with versionptr <ptr>."""
    return map(dump_spec, Spec.objects.filter(version__versionptr=versionptr))
    
def specs_snippets(request, versionptr):
    """GET /api/specs/<ptr>/snippets/ : Get all snippets associated with the spec versionptr <ptr>."""
    objs = Snippet.objects.filter(spec_versionptr = versionptr)
    return map(dump_snippet, objs)

def specs_snippets_active(request, versionptr):
    """GET /api/specs/<ptr>/snippets/active/ : Gets the current active snippet in each language on the given spec versionptr"""
    objs = Snippet.objects.filter(spec_versionptr=versionptr, version__active=True)
    return map(dump_snippet, objs)

def spec(request, version):
    """GET /api/spec/<ver>/ : Get the spec at version <ver>."""
    return dump_spec(Spec.objects.get(version=version))

def snippets_active(request, versionptr):
    """GET /api/snippets/<ptr>/active/ : Gets the current active snippet associated with snippet versionptr <ptr>."""
    return dump_snippet(Snippet.objects.get(version__versionptr=versionptr, version__active=True))

def snippets_all(request, versionptr):
    """GET /api/snippets/<ptr>/all/ : Gets all versions of snippets associated with snippet versionptr <ptr>."""
    return map(dump_snippet, Snippet.objects.filter(version__versionptr=versionptr))

def snippet(request, version):
    """GET /api/snippet/<ver>/ : Gets the snippet at version <ver>."""
    return dump_snippet(Snippet.objects.get(version=version))

def bugs(request, versionptr):
    """GET /api/specs/<ptr>/bugs/active/
       GET /api/snippets/<ptr>/bugs/active/

    Gets all the active bugs on a snippet or spec.
    """

    bugs = BugReport.objects.filter(target_versionptr=versionptr, version__active=True)
    return map(dump_bug, bugs)

def bugs_all(request, versionptr):
    """GET /api/bugs/<ptr>/all/: gets all versions of bugs associated with bug versionptr <ptr>"""
    return map(dump_bug, BugReport.objects.filter(version__versionptr=versionptr).order_by('version__timestamp'))

def bug(request, version):
    """GET /api/bug/<ver>/: get a specific bug version"""
    return dump_bug(BugReport.objects.get(version=version))

def maybe(value, defined, undefined=None):
    if value is None:
        return undefined
    else:
        return defined(value)

@login_required
def new_spec(request):
    """POST /api/new/spec/ : Creates a new spec.

        versionptr: (optional) what versionptr to add this version to.
                    Allocates new if not given.
        name: (optional) Name of this spec ("unnamed" if not given)
        summary: (optional) Summary of this spec ("" if not given)
        spec: (optinal) Description of this spec ("" if not given)
        comment: (optional) Description of this change
    """
    versionptr = get_or_new_versionptr('Spec', request.POST.get('versionptr'))

    # TODO leave inactive if user is untrusted
    version = new_version(request.user, versionptr, request.POST.get('comment') or "")
    version.save()

    spec = Spec(
        version=version,
        name=request.POST.get('name') or "unnamed", 
        summary=request.POST.get('summary') or "",
        spec=request.POST.get('spec') or "",
        status=maybe(request.POST.get('status'), lambda x: Spec.STATUS_TO_ID[x], 0))
    spec.save()

    update_active(versionptr)
    notify_followers(request.user, versionptr)
    follow(request.user, versionptr, True)

    return {
        'versionptr': versionptr.id,
        'version': version.id,
    }

@login_required
def new_snippet(request):
    """POST /api/new/snippet/ : Creates a new snippet.

        spec_versionptr : what spec versionptr to associate this code with
        versionptr : (optional) what versionptr to make a new version of. 
                     Allocates new versionptr if not given.
        code : The code in the snippet
        language : The language the snippet is wirtten in
        dependencies : (optional) A comma-separated list of spec versionptrs the snippet depends on
        comment: (optional) Description of this change
    """
    
    spec_versionptr = VersionPtr.objects.get(id=int(request.POST['spec_versionptr']))
    versionptr = get_or_new_versionptr('Snippet', request.POST.get('versionptr'))

    version = new_version(request.user, versionptr, request.POST.get('comment') or "")
    version.save()

    code = request.POST['code'].strip() + "\n"
    
    snippet = Snippet(version=version, 
                      code=code, 
                      language=request.POST['language'],
                      spec_versionptr=spec_versionptr)
    snippet.save()

    deps = request.POST.get('dependencies')
    if deps:
        for dep in deps.split(','):
            Dependency(snippet=snippet, target=VersionPtr.objects.get(id=int(dep))).save()

    update_active(versionptr)
    notify_followers(request.user, versionptr)
    follow(request.user, versionptr, True)

    return {
        'versionptr': versionptr.id,
        'version': version.id,
    }

def new_bug(request):
    """POST /api/new/bug/ : Creates a new bug report (or modifies an exisitng one)

        target_versionptr : what spec/snippet versionptr to associate this report with
        versionptr : (optional) what bug versionptr to put this bug in sequence with.
                     Allocates new versionptr if not given.
        title : The title of the bug
        status : "Open", "Resolved" or "Closed"
        comment: (optional) Description of this change or comments on the bug
    """
    
    target_versionptr = VersionPtr.objects.get(id=int(request.POST['target_versionptr']))
    versionptr = get_or_new_versionptr('BugReport', request.POST.get('versionptr'))

    status = BugReport.STATUS_TO_ID[request.POST['status']]

    version = new_version(request.user, versionptr, request.POST.get('comment') or "")
    version.save()

    bug = BugReport(version=version, 
                    title=request.POST['title'], 
                    target_versionptr=target_versionptr,
                    status=status)
    bug.save()

    update_active(versionptr)
    notify_followers(request.user, target_versionptr)
    notify_followers(request.user, versionptr)
    follow(request.user, versionptr, True)

    return {
        'versionptr': versionptr.id,
        'version': version.id,
    }

def search(request):
    """GET /api/search/?q=text : Search for specs matching the given text."""

    results = SearchQuerySet().auto_query(request.GET['q'])[0:10]
    return [ { 'name': r.name,
               'summary': r.summary,
               'versionptr': r.versionptrid } 
                        for r in results ]

@login_required
def user_update(request):
    """POST /api/user/update/ : Update the details of a user

        id: the user id of the user to update
        username, first_name, last_name, email are all required
    """
    user = User.objects.get(id=request.POST['id'])
    user.username = request.POST['username']
    user.first_name = request.POST['first_name']
    user.last_name = request.POST['last_name']
    user.email = request.POST['email']
    user.save()
    return ""

def follow(user, versionptr, enabled):
    if user.is_anonymous(): return
    fset = Following.objects.filter(follower=user, followed=versionptr)
    if not enabled:
        fset.delete()
    elif not fset.exists():
        Following.objects.create(
            follower=user, 
            followed=versionptr,
            new_events=False, 
            last_check=datetime.now())
    

@login_required
def user_follow(request):
    """POST /api/user/follow/ : Have the authenticated user subscribe to any changes of a versionptr

        versionptr: the versionptr to follow
        enabled: (optional) If False, remove instead of add the follow relation.
    """
    enabled = request.POST.get('enabled')
    if enabled is None: enabled = True
    follow(request.user, request.POST['versionptr'], enabled)
    return ""

def user_events_check(request):
    """GET /api/user/events/check/ : Returns a boolean indicating whether there are new events for the logged in user"""
    
    return Following.objects.filter(follower=request.user, new_events=True).exists()

def user_events_new(request):
    """GET /api/user/events/new/ : Get all unseen events that the user is subscribed to"""
    
    fset = Following.objects.filter(follower=request.user, new_events=True)
    ret = []
    now = datetime.now()
    for fol in fset:
        ret.extend(get_events_date_range(fol.followed, fol.last_check, now))
    return ret

@login_required
def user_events_mark_viewed(request):
    """POST /api/user/events/mark_viewed/ : Mark a versionptr as viewed.

        versionptr: the versionptr to mark as viewed
    """

    Following.objects.filter(follower=request.user, new_events=True, followed=request.POST['versionptr']).update(new_events=False, last_check=datetime.now())
    
    return ""

# CodeCatalog Snippet http://www.codecatalog.net/91/253/
import random
# End CodeCatalog Snippet

# CodeCatalog Snippet http://www.codecatalog.net/179/472/
def random_hex_string(length):
    return ''.join("0123456789abcdef"[random.randint(0,15)] for i in range(length))
# End CodeCatalog Snippet

@login_required
def user_make_api_key(request):
    """POST /api/user/make_api_key/ : Make and return a new API key."""

    if request.user.is_authenticated():
        pwd = random_hex_string(32)
        request.user.set_password(pwd)
        request.user.save()
        return pwd
    else:
        return None

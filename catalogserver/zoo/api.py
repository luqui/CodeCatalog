from zoo.models import *
from datetime import datetime
from haystack.query import SearchQuerySet
from django.db.models import Q

# Versions are organized into versionptrs, which essentially represents
# a collection of versions of the same thing.  When we view a spec or a
# snippet on the site, we refer to it using a versionptr, and we see
# the latest active version.
# Versions and versionptrs are separate, numeric namespaces. Versionptr 1
# and version 1 are not related.

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
    print "Name = " + name
    for v in Version.objects.filter(versionptr=versionptr, timestamp__gt=startdate, timestamp__lt=enddate):
        events.append({
            'type': 'new_version',
            'versionptr': versionptr.id,
            'versionptr_type': versionptr_type,
            'version': v.id,
            'timestamp': v.timestamp.isoformat(),
            'name': name,
        })
    for v in Vote.objects.filter(versionptr=versionptr, timestamp__gt=startdate, timestamp__lt=enddate):
        events.append({
            'type': 'vote',
            'versionptr': versionptr.id,
            'versionptr_type': versionptr_type,
            'timestamp': v.timestamp.isoformat(),
            'value': v.value,
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
        'votes': spec.version.versionptr.votes,
        'timestamp': spec.version.timestamp.isoformat(),
        'comment': spec.version.comment,
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
        'votes': snippet.version.versionptr.votes,
        'timestamp': snippet.version.timestamp.isoformat(),
        'comment': snippet.version.comment,
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
        'user': bug.version.user.username,
    }
        

# Begin CodeCatalog Snippet http://codecatalog.net/20/
def traverse_cons_list(conslist):
    while conslist is not ():
        (x,xs) = conslist
        yield x
        conslist = xs
# End CodeCatalog Snippet

# Begin CodeCatalog Snippet http://codecatalog.net/25/
import heapq
# End CodeCatalog Snippet

# Begin CodeCatalog Snippet http://codecatalog.net/30/
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


def assemble(request, versionptr):
    """GET /api/specs/<ptr>/assemble/ : Get a list of snippets which transitively assemble a spec"""
    def children(elem):
        (vptr, rest) = (elem[0], elem[1:])
        snips = Snippet.objects.filter(spec_versionptr=vptr, version__active=True)
        return (( -snip.version.versionptr.votes
                , snip.dependency_set.values_list('target', flat=True)
                , snip ) 
                for snip in snips)
    def success(elem):
        return len(elem) == 0
    return map(dump_snippet, shortest_path(children, success, (versionptr,)) or ()) or None

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

    spec = Spec(version=version, name=request.POST.get('name') or "unnamed", summary=request.POST.get('summary') or "", spec=request.POST.get('spec') or "")
    spec.save()

    update_active(versionptr)
    notify_followers(request.user, versionptr)
    follow(request.user, versionptr, True)

    return {
        'versionptr': versionptr.id,
        'version': version.id,
    }

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

def vote(request):
    """POST /api/vote/ : Votes on a versionptr.  Cancels out any previous vote.

        versionptr: the versionptr to vote on
        value: -1, 0, or 1"""

    # TODO Proper error handling anyone?
    if not request.user.is_authenticated: return ""
    
    # TODO race condition
    versionptr = VersionPtr.objects.get(id=request.POST['versionptr'])
    value = int(request.POST['value'])
    
    pvotes = Vote.objects.filter(user=request.user, versionptr=versionptr)
    for pvote in pvotes:
        versionptr.votes -= pvote.value
    pvotes.delete()
    
    if value != 0:
        vote = Vote(user=request.user, versionptr=versionptr, value=value, timestamp=datetime.now())
        versionptr.votes += value
        vote.save()
    versionptr.save()

    notify_followers(request.user, versionptr)

    return ""

def search(request):
    """GET /api/search/?q=text : Search for specs matching the given text."""

    results = SearchQuerySet().auto_query(request.GET['q'])[0:10]
    return [ { 'name': r.object.name, 'summary': r.object.summary, 'version': r.object.version.id, 'versionptr': r.object.version.versionptr.id } 
                        for r in results ]

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

def user_events_mark_viewed(request):
    """POST /api/user/events/mark_viewed/ : Mark a versionptr as viewed.

        versionptr: the versionptr to mark as viewed
    """

    Following.objects.filter(follower=request.user, new_events=True, followed=request.POST['versionptr']).update(new_events=False, last_check=datetime.now())
    
    return ""

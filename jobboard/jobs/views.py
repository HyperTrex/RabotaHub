from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from urllib.parse import urlencode
from datetime import datetime
from accounts.models import Profile
from django.contrib.auth.models import User
from .models import Application, Job, SavedJob, Message


def is_employer(user):
    return hasattr(user, 'profile') and user.profile.user_type == 'employer'


def home(request):
    featured_jobs = Job.objects.select_related('employer').order_by('-created_at')[:6]
    hiring_companies = list(
        Job.objects.exclude(employer__profile__company_name='')
        .order_by('employer__profile__company_name')
        .values_list('employer__profile__company_name', flat=True)
        .distinct()[:8]
    )
    stats = {
        'jobs': Job.objects.count(),
        'employers': Profile.objects.filter(user_type='employer').count(),
        'applications': Application.objects.count(),
        'seekers': Profile.objects.filter(user_type='seeker').count(),
    }

    # Get user type if authenticated
    user_type = None
    if request.user.is_authenticated:
        try:
            user_type = request.user.profile.user_type
        except Profile.DoesNotExist:
            pass

    return render(request, 'jobs/home.html', {
        'featured_jobs': featured_jobs,
        'hiring_companies': hiring_companies,
        'stats': stats,
        'user_type': user_type,
        'user': request.user,
    })


def set_language(request, language):
    if language in ['mk', 'en']:
        request.session['language'] = language

    return redirect(request.GET.get('next') or 'home')


def about(request):
    # Get user type if authenticated
    user_type = None
    if request.user.is_authenticated:
        try:
            user_type = request.user.profile.user_type
        except Profile.DoesNotExist:
            pass
    return render(request, 'jobs/about.html', {'user_type': user_type})


def contact(request):
    # Get user type if authenticated
    user_type = None
    if request.user.is_authenticated:
        try:
            user_type = request.user.profile.user_type
        except Profile.DoesNotExist:
            pass
    return render(request, 'jobs/contact.html', {'user_type': user_type})


def privacy(request):
    # Get user type if authenticated
    user_type = None
    if request.user.is_authenticated:
        try:
            user_type = request.user.profile.user_type
        except Profile.DoesNotExist:
            pass
    return render(request, 'jobs/privacy.html', {'user_type': user_type})


def terms(request):
    # Get user type if authenticated
    user_type = None
    if request.user.is_authenticated:
        try:
            user_type = request.user.profile.user_type
        except Profile.DoesNotExist:
            pass
    return render(request, 'jobs/terms.html', {'user_type': user_type})


def job_list(request):
    jobs = Job.objects.select_related('employer').order_by('-created_at')
    applied_jobs = []
    saved_jobs = []

    q = request.GET.get('q', '').strip()
    category = request.GET.get('category', '').strip()
    location = request.GET.get('location', '').strip()
    min_salary = request.GET.get('min_salary', '').strip()

    if q:
        jobs = jobs.filter(title__icontains=q)

    if category:
        jobs = jobs.filter(category=category)

    if location:
        jobs = jobs.filter(location__icontains=location)

    if min_salary.isdigit():
        jobs = jobs.filter(salary__gte=min_salary)

    # Get user type if authenticated
    user_type = None
    if request.user.is_authenticated:
        applied_jobs = Application.objects.filter(
            applicant=request.user
        ).values_list('job_id', flat=True)
        saved_jobs = SavedJob.objects.filter(
            user=request.user
        ).values_list('job_id', flat=True)
        try:
            user_type = request.user.profile.user_type
        except Profile.DoesNotExist:
            pass

    paginator = Paginator(jobs, 6)
    page = request.GET.get('page')
    jobs = paginator.get_page(page)

    # Build current filters string for pagination (preserve all filters except page)
    current_filters = request.GET.copy()
    if 'page' in current_filters:
        del current_filters['page']
    current_filters = current_filters.urlencode() if current_filters else ""

    return render(request, 'jobs/job_list.html', {
        'jobs': jobs,
        'applied_jobs': applied_jobs,
        'saved_jobs': saved_jobs,
        'filters': {
            'q': q,
            'category': category,
            'location': location,
            'min_salary': min_salary,
        },
        'categories': Job.CATEGORY_CHOICES,
        'current_filters': current_filters,
        'user_type': user_type,
    })


@login_required
def create_job(request):
    if not is_employer(request.user):
        return redirect('job_list')

    if request.method == 'POST':
        company_name = request.POST.get('company_name', '').strip()
        if company_name:
            request.user.profile.company_name = company_name
            request.user.profile.save()

        Job.objects.create(
            title=request.POST['title'],
            description=request.POST['description'],
            requirements=request.POST['requirements'],
            salary=request.POST['salary'],
            location=request.POST['location'],
            category=request.POST['category'],
            employer=request.user
        )
        return redirect('dashboard')

    # Get user type
    user_type = None
    try:
        user_type = request.user.profile.user_type
    except Profile.DoesNotExist:
        pass

    return render(request, 'jobs/create_job.html', {
        'categories': Job.CATEGORY_CHOICES,
        'user_type': user_type,
    })


@login_required
def apply_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    if is_employer(request.user):
        return redirect('job_detail', job_id=job.id)

    if Application.objects.filter(job=job, applicant=request.user).exists():
        return redirect('job_detail', job_id=job.id)

    if request.method == 'POST':
        # Handle file upload
        resume_file = request.FILES.get('resume') if 'resume' in request.FILES else None
        
        # Handle date field
        start_date = request.POST.get('start_date')
        start_date_obj = datetime.strptime(start_date, '%Y-%m-%d').date() if start_date else None
        
        Application.objects.create(
            job=job,
            applicant=request.user,
            message=request.POST.get('message', ''),
            phone=request.POST.get('phone', ''),
            email=request.POST.get('email', ''),
            linkedin_url=request.POST.get('linkedin_url', ''),
            github_url=request.POST.get('github_url', ''),
            portfolio_url=request.POST.get('portfolio_url', ''),
            resume=resume_file,
            work_eligibility=request.POST.get('work_eligibility', ''),
            start_date=start_date_obj,
            cover_letter=request.POST.get('cover_letter', '')
        )
        return redirect('job_detail', job_id=job.id)

    # Get user type
    user_type = None
    try:
        user_type = request.user.profile.user_type
    except Profile.DoesNotExist:
        pass

    return render(request, 'jobs/apply.html', {
        'job': job,
        'user_type': user_type,
    })


@login_required
def save_job(request, job_id):
    if is_employer(request.user):
        return redirect('job_detail', job_id=job_id)

    job = get_object_or_404(Job, id=job_id)
    saved_job, created = SavedJob.objects.get_or_create(user=request.user, job=job)

    if not created:
        saved_job.delete()

    return redirect(request.GET.get('next') or 'job_list')


@login_required
def saved_jobs(request):
    saved = SavedJob.objects.select_related(
        'job',
        'job__employer',
    ).filter(user=request.user).order_by('-id')

    # Get user type
    user_type = None
    try:
        user_type = request.user.profile.user_type
    except Profile.DoesNotExist:
        pass

    return render(request, 'jobs/saved_jobs.html', {
        'saved': saved,
        'user_type': user_type,
    })


def job_detail(request, job_id):
    job = get_object_or_404(Job.objects.select_related('employer'), id=job_id)
    has_applied = False
    is_saved = False
    user_type = None

    if request.user.is_authenticated:
        has_applied = Application.objects.filter(job=job, applicant=request.user).exists()
        is_saved = SavedJob.objects.filter(job=job, user=request.user).exists()
        try:
            user_type = request.user.profile.user_type
        except Profile.DoesNotExist:
            pass

    return render(request, 'jobs/job_detail.html', {
        'job': job,
        'has_applied': has_applied,
        'is_saved': is_saved,
        'user_type': user_type,
    })


@login_required
def employer_dashboard(request):
    if not is_employer(request.user):
        return redirect('job_list')

    jobs = Job.objects.filter(employer=request.user).order_by('-created_at')

    data = []
    total_applications = 0
    for job in jobs:
        applications = Application.objects.filter(job=job).select_related('applicant')
        total_applications += applications.count()
        data.append({
            'job': job,
            'applications': applications,
        })

    # Get user type
    user_type = None
    try:
        user_type = request.user.profile.user_type
    except Profile.DoesNotExist:
        pass

    return render(request, 'jobs/dashboard.html', {
        'data': data,
        'total_jobs': jobs.count(),
        'total_applications': total_applications,
        'user_type': user_type,
    })


@login_required
def user_profile(request):
    # Get user type
    user_type = None
    try:
        user_type = request.user.profile.user_type
    except Profile.DoesNotExist:
        pass

    # Get statistics based on user type
    context = {'user_type': user_type}
    
    if user_type == 'seeker':
        context['saved_jobs_count'] = SavedJob.objects.filter(user=request.user).count()
        context['applications_count'] = Application.objects.filter(applicant=request.user).count()
    elif user_type == 'employer':
        context['posted_jobs_count'] = Job.objects.filter(employer=request.user).count()
        context['received_applications_count'] = Application.objects.filter(job__employer=request.user).count()

    return render(request, 'jobs/profile.html', context)


@login_required
def notifications(request):
    # Get user type
    user_type = None
    try:
        user_type = request.user.profile.user_type
    except Profile.DoesNotExist:
        pass

    return render(request, 'jobs/notifications.html', {
        'user_type': user_type,
    })


@login_required
def messages(request):
    # Get user type
    user_type = None
    try:
        user_type = request.user.profile.user_type
    except Profile.DoesNotExist:
        pass

    # Get user's messages
    received_messages = Message.objects.filter(recipient=request.user).select_related('sender', 'sender__profile')
    sent_messages = Message.objects.filter(sender=request.user).select_related('recipient', 'recipient__profile')
    
    # Calculate counts
    received_count = received_messages.count()
    sent_count = sent_messages.count()
    unread_count = received_messages.filter(is_read=False).count()
    
    # Mark as read when viewing
    received_messages.filter(is_read=False).update(is_read=True)

    return render(request, 'jobs/messages.html', {
        'user_type': user_type,
        'received_messages': received_messages,
        'sent_messages': sent_messages,
        'received_count': received_count,
        'sent_count': sent_count,
        'unread_count': unread_count,
    })


@login_required
def compose_message(request):
    # Get user type
    user_type = None
    try:
        user_type = request.user.profile.user_type
    except Profile.DoesNotExist:
        pass

    if request.method == 'POST':
        recipient_username = request.POST.get('recipient')
        subject = request.POST.get('subject')
        body = request.POST.get('body')
        job_id = request.POST.get('job_id')

        try:
            recipient = User.objects.get(username=recipient_username)
            
            # Check if job exists and user has access
            job = None
            if job_id:
                job = get_object_or_404(Job, id=job_id)
                # Ensure sender can message about this job
                if job.employer != request.user and not Application.objects.filter(job=job, applicant=request.user).exists():
                    job = None

            Message.objects.create(
                sender=request.user,
                recipient=recipient,
                subject=subject,
                body=body,
                job=job
            )
            return redirect('messages')
        except User.DoesNotExist:
            # Error handling for invalid recipient
            pass

    # Get list of possible recipients
    possible_recipients = User.objects.exclude(id=request.user.id).select_related('profile')
    
    # Get job if specified
    job = None
    job_id = request.GET.get('job_id')
    if job_id:
        job = get_object_or_404(Job, id=job_id)
        # Pre-fill recipient based on job
        if job.employer != request.user:
            possible_recipients = possible_recipients.filter(id=job.employer.id)

    return render(request, 'jobs/compose_message.html', {
        'user_type': user_type,
        'possible_recipients': possible_recipients,
        'job': job,
    })


@login_required
def message_detail(request, message_id):
    # Get user type
    user_type = None
    try:
        user_type = request.user.profile.user_type
    except Profile.DoesNotExist:
        pass

    message = get_object_or_404(Message, id=message_id)
    
    # Check if user has access to this message
    if message.sender != request.user and message.recipient != request.user:
        return redirect('messages')
    
    # Mark as read if recipient
    if message.recipient == request.user:
        message.is_read = True
        message.save()

    return render(request, 'jobs/message_detail.html', {
        'user_type': user_type,
        'message': message,
    })

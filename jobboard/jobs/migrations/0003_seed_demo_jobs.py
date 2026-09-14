from django.db import migrations


EMPLOYERS = [
    ('vardar_tech', 'Vardar Tech'),
    ('skopje_digital', 'Skopje Digital Studio'),
    ('pelagonia_finance', 'Pelagonia Finance'),
    ('ohrid_travel_group', 'Ohrid Travel Group'),
    ('nova_retail', 'Nova Retail'),
    ('urban_creative', 'Urban Creative Lab'),
    ('balkan_cloud', 'Balkan Cloud Solutions'),
    ('green_logistics', 'Green Logistics MK'),
]

SEEKERS = [
    'ana_markovska',
    'filip_stojanov',
    'elena_petrova',
    'martin_iliev',
    'sara_trajkovska',
]

JOBS = [
    ('Senior Backend Developer', 'IT', 'Skopje / Hybrid', 95000, 'Vardar Tech', 'Build reliable APIs, integrations, and internal services for high-traffic products used by regional clients.', 'Django or Node experience, PostgreSQL, REST APIs, Git, and strong debugging skills.'),
    ('Frontend React Engineer', 'IT', 'Skopje', 78000, 'Skopje Digital Studio', 'Create polished dashboards, booking flows, and responsive customer portals for SaaS clients.', 'React, JavaScript, HTML/CSS, component thinking, and experience consuming APIs.'),
    ('Junior QA Tester', 'IT', 'Bitola', 42000, 'Balkan Cloud Solutions', 'Test web applications, document bugs, and help engineering teams ship cleaner releases.', 'Attention to detail, basic SQL, test case writing, and curiosity about automation.'),
    ('DevOps Engineer', 'IT', 'Remote', 105000, 'Balkan Cloud Solutions', 'Maintain CI/CD pipelines, cloud deployments, monitoring, and production infrastructure.', 'Linux, Docker, cloud platforms, scripting, and incident response experience.'),
    ('Data Analyst', 'IT', 'Skopje', 69000, 'Pelagonia Finance', 'Turn business data into dashboards and insights for finance, risk, and product teams.', 'SQL, Excel, BI tools, analytical thinking, and clear communication.'),
    ('IT Support Specialist', 'IT', 'Tetovo', 43000, 'Nova Retail', 'Support retail teams with hardware, software, networks, and internal tools.', 'Windows support, basic networking, ticketing systems, and calm customer communication.'),
    ('Product Designer', 'Design', 'Skopje / Hybrid', 74000, 'Urban Creative Lab', 'Design user flows, wireframes, prototypes, and production-ready interfaces for digital products.', 'Figma, UX research, design systems, prototyping, and portfolio of shipped work.'),
    ('Graphic Designer', 'Design', 'Ohrid', 48000, 'Ohrid Travel Group', 'Create campaigns, social visuals, print materials, and brand assets for tourism offers.', 'Adobe Creative Suite or Figma, layout skills, typography, and social media formats.'),
    ('UX Research Assistant', 'Design', 'Remote', 46000, 'Urban Creative Lab', 'Plan interviews, summarize findings, and help product teams understand user needs.', 'Interviewing, note synthesis, empathy, structured thinking, and concise writing.'),
    ('Motion Designer', 'Design', 'Skopje', 62000, 'Skopje Digital Studio', 'Produce short animations, product videos, and campaign motion assets.', 'After Effects, timing, visual storytelling, and asset preparation.'),
    ('Digital Marketing Specialist', 'Marketing', 'Skopje', 56000, 'Nova Retail', 'Manage paid campaigns, email promotions, and weekly performance reporting.', 'Meta/Google Ads, analytics, copywriting, and campaign optimization.'),
    ('SEO Content Writer', 'Marketing', 'Remote', 45000, 'Skopje Digital Studio', 'Write search-friendly articles, landing pages, and product content for local and global clients.', 'SEO basics, Macedonian and English writing, research skills, and CMS experience.'),
    ('Social Media Manager', 'Marketing', 'Ohrid', 52000, 'Ohrid Travel Group', 'Plan and publish content for travel campaigns, events, and seasonal offers.', 'Content calendar planning, community management, photography sense, and reporting.'),
    ('Brand Strategist', 'Marketing', 'Skopje / Hybrid', 81000, 'Urban Creative Lab', 'Shape brand positioning, campaign narratives, and go-to-market messaging.', 'Strategy workshops, market research, storytelling, and client presentation skills.'),
    ('Performance Marketing Analyst', 'Marketing', 'Skopje', 70000, 'Pelagonia Finance', 'Analyze acquisition funnels, campaign ROI, and customer behavior.', 'Analytics tools, spreadsheets, attribution thinking, and clear recommendations.'),
    ('Customer Success Specialist', 'Other', 'Skopje', 47000, 'Vardar Tech', 'Onboard customers, answer product questions, and collect feedback for product teams.', 'Communication skills, SaaS tools, problem solving, and Macedonian/English fluency.'),
    ('HR Recruiter', 'Other', 'Skopje', 54000, 'Green Logistics MK', 'Source candidates, coordinate interviews, and improve hiring workflows.', 'Recruiting experience, structured interviews, organization, and people skills.'),
    ('Finance Assistant', 'Other', 'Bitola', 44000, 'Pelagonia Finance', 'Support invoices, payments, reconciliations, and monthly reporting.', 'Excel, accuracy, accounting basics, and confidentiality.'),
    ('Operations Coordinator', 'Other', 'Kumanovo', 50000, 'Green Logistics MK', 'Coordinate shipments, schedules, suppliers, and daily operational updates.', 'Organization, communication, Excel, and ability to solve urgent issues.'),
    ('Sales Representative', 'Other', 'Skopje', 58000, 'Nova Retail', 'Build relationships with business customers and grow monthly sales pipelines.', 'Sales experience, negotiation, CRM discipline, and field readiness.'),
    ('Travel Experience Agent', 'Other', 'Ohrid', 42000, 'Ohrid Travel Group', 'Help guests choose tours, resolve questions, and deliver excellent travel support.', 'Customer service, English, local tourism knowledge, and friendly communication.'),
    ('Mobile App Developer', 'IT', 'Remote', 88000, 'Vardar Tech', 'Develop mobile features for Android and iOS products used by service teams.', 'React Native or Flutter, API integration, app store basics, and testing discipline.'),
    ('E-commerce Manager', 'Marketing', 'Skopje', 76000, 'Nova Retail', 'Own online store performance, merchandising, campaigns, and conversion improvements.', 'E-commerce tools, analytics, product catalog work, and commercial thinking.'),
    ('UI Designer', 'Design', 'Remote', 61000, 'Urban Creative Lab', 'Create detailed screens, reusable components, and visual systems for modern web apps.', 'Figma, visual design, responsive layouts, and strong attention to polish.'),
]


def seed_jobs(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    Profile = apps.get_model('accounts', 'Profile')
    Job = apps.get_model('jobs', 'Job')
    Application = apps.get_model('jobs', 'Application')

    employers_by_company = {}
    for username, company_name in EMPLOYERS:
        user, _ = User.objects.get_or_create(username=username, defaults={
            'email': f'{username}@example.com',
            'is_active': True,
        })
        Profile.objects.get_or_create(user=user, defaults={
            'user_type': 'employer',
            'company_name': company_name,
        })
        profile = Profile.objects.get(user=user)
        if profile.company_name != company_name:
            profile.company_name = company_name
            profile.save()
        employers_by_company[company_name] = user

    seekers = []
    for username in SEEKERS:
        user, _ = User.objects.get_or_create(username=username, defaults={
            'email': f'{username}@example.com',
            'is_active': True,
        })
        Profile.objects.get_or_create(user=user, defaults={'user_type': 'seeker'})
        seekers.append(user)

    for index, (title, category, location, salary, company, description, requirements) in enumerate(JOBS):
        employer = employers_by_company[company]
        job, _ = Job.objects.get_or_create(
            title=title,
            employer=employer,
            defaults={
                'category': category,
                'location': location,
                'salary': salary,
                'description': description,
                'requirements': requirements,
            }
        )

        if index < 10:
            applicant = seekers[index % len(seekers)]
            Application.objects.get_or_create(
                job=job,
                applicant=applicant,
                defaults={
                    'message': 'Имам релевантно искуство и би сакал/а да разговараме за позицијата.'
                }
            )


def remove_seed_jobs(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    Job = apps.get_model('jobs', 'Job')

    employer_usernames = [username for username, _ in EMPLOYERS]
    seeker_usernames = SEEKERS
    Job.objects.filter(employer__username__in=employer_usernames).delete()
    User.objects.filter(username__in=employer_usernames + seeker_usernames).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        ('jobs', '0002_savedjob'),
    ]

    operations = [
        migrations.RunPython(seed_jobs, remove_seed_jobs),
    ]

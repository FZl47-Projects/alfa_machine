from public.models import ProjectFile, Department

files = ProjectFile.objects.all()
for file in files:
    file.to_departments.set(Department.objects.all())

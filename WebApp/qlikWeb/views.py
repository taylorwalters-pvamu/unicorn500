from django.shortcuts import render
from django.http import HttpResponse
from qlikWeb.forms import UserForm

def index(request):
    if request.method == 'POST':
        # Get user selections
        selected_options = {key: request.POST[key] for key in request.POST.keys() if key.startswith('dropdown_')}

        # Generate Qlik Sense script based on user selections
        qlik_script = generate_qlik_script(selected_options)

        # Save or execute the script as needed

        return HttpResponse(f"Generated Qlik Sense script: {qlik_script}")

    dropdown_options = {
        '''Drop down options for data transfer.
        Dimension 1 should list system options
        Dimension 2 should list data column selections for transfer.
        '''

        'dimension1': ['Option1', 'Option2', 'Option3'],
        'dimension2': ['OptionA', 'OptionB', 'OptionC']
    }

    return render(request, 'qlikWeb/index.html', {'dropdown_options': dropdown_options})

def generate_qlik_script(selected_options):
    # Implement logic to generate Qlik Sense script based on user selections
    # Use selected_options dictionary to customize the script
    return "Generated Qlik Sense script based on user selections"

def adapter(request):
    form = UserForm()
    context = {}
    context['title']='Login'
    context['form']= form
    if request.method == 'POST':
        form = UserForm(request, data=request.POST)
        if form.is_valid():
            return render(request, 'qlik.com')
    else:
        form = UserForm()
    
    return render(request, 'adapter.html', context)

def about(request):
    context = {}
    context['title']= 'About'
    return render(request, 'about.html')

def index(request):
    context = {}
    context['title']= 'Index'
    return render(request, 'index.html')

def demo(request):
    context = {}
    context['title']= 'How it works'
    return render(request, 'demo.html')

def support(request):
    context = {}
    context['title']= 'Support Ticket'
    return render(request, 'support.html')

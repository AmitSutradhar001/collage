from django import forms

class StForm(forms.Form):
    message = forms.CharField( label='', widget=forms.Textarea(attrs={
        'placeholder': 'Enter your message here',
        'rows': 5,
        'cols': 40,
        'class': 'w-full p-3 border rounded-md focus:ring focus:ring-blue-300 focus:outline-none'  # Optional for styling with CSS or frameworks
    }))    
    img = forms.ImageField(
        label='',  # Remove the label
        widget=forms.ClearableFileInput(attrs={
            'class': 'block outline-none w-full text-sm text-gray-600 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-gray-200 hover:file:bg-gray-300',  # Add custom CSS classes
            'style': 'border: 2px solid #ccc; padding: 10px;',  # Inline styling
            'accept': 'image/*',  # Optional: Limit file selection to images
        }))
class DecodeForm(forms.Form):
    img = forms.ImageField(
        label='',  # Remove the label
        widget=forms.ClearableFileInput(attrs={
            'class': 'block outline-none w-full text-sm text-gray-600 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-gray-200 hover:file:bg-gray-300 border-2',  # Add custom CSS classes
            'style': 'border: 2px solid #ccc; padding: 10px;',  # Inline styling
            'accept': 'image/*',  # Optional: Limit file selection to images
        }))
from django.shortcuts import render
import os
import re
import subprocess
import google.generativeai as genai
from django.views import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView


# Configure Gemini API
os.environ["GEMINI_API_KEY"] = "AIzaSyAtQuDqLhgj90hxKGv9W31kThYVSD2PHLg"
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

class RunTerraform(TemplateView):
    template_name = "terraform.html"
    def post(self, request):
        self.message = ""
        try:
            body = request.POST
            prompt = body["prompt"]

            model = genai.GenerativeModel("gemini-1.5-pro-latest")
            response = model.generate_content(f"""
            You are an expert in Terraform and Infrastructure as Code.
            Generate valid Terraform code inside triple backticks (```hcl ... ```).
            Do not include any explanations, comments, or extra text.
            Include a provider block. Just return the Terraform code.
            Use string interpolation with ${{}} instead of using + directly in resource
            arn
            Request: {prompt}
            """)

            response_text = response.text if hasattr(response, 'text') else response.parts[0].text
            match = re.search(r"```(?:hcl)?\n(.*?)\n```", response_text, re.DOTALL)
            if match:
                terraform_code = match.group(1).strip()
            else:
                terraform_code = response_text.strip()
            
            self.run_terraform(terraform_code)
            clean_message = re.sub(r'\x1b\[[0-9;]*m', '', self.message)
            return render(request, self.template_name, {"message": clean_message})
        except Exception as err:
            return render(request, self.template_name, {"message": self.message, "error": str(err)})

    # Enhanced Recommendations Function
    def get_recommendations(prompt):
        model = genai.GenerativeModel("gemini-1.5-pro-latest")
        response = model.generate_content(f"""
        A user deployed this Terraform service: \"\"\"{prompt}\"\"\"
        Provide exactly 4 enhancements (optimization, security, performance, usability).
        Use only hyphen bullets. Format: "- <recommendation>"
        No explanations or extra text.
        """)

        response_text = response.text if hasattr(response, 'text') else response.parts[0].text
        recommendations = re.findall(r'-\s*(.+?)\s*$', response_text, re.MULTILINE)
        return recommendations[:4] if recommendations else ["⚠️ No recommendations available"]

    # Terraform Execution Functions
    def run_terraform_command(self, command, aws_env):
        try:
            result = subprocess.run(command, check=True, capture_output=True, text=True, env={**os.environ, **aws_env} )
            success_msg = f"✅ {' '.join(command)} succeeded!\n{result.stdout}"
            print(success_msg)
            self.message += success_msg + "\n"
            return True
        except subprocess.CalledProcessError as e:
            error_msg = f"❌ Error: {' '.join(command)}\n{e.stderr}"
            print(error_msg)
            self.message += error_msg + "\n"
            return False

    def run_terraform(self, terraform_code):
        aws_env = {
            "AWS_ACCESS_KEY_ID": "AKIAYKFQQ6SE3FQ34QCZ",
            "AWS_SECRET_ACCESS_KEY": "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",
            "AWS_DEFAULT_REGION": "us-east-1",
            "AWS_DEFAULT_OUTPUT": "json"
        }
        try:
            os.makedirs("terraform_workspace", exist_ok=True)
            os.chdir("terraform_workspace")
            with open("main.tf", "w") as f:
                f.write(terraform_code)

            print("✅ Code written to main.tf")
            self.message += "✅ Code written to main.tf" + "\n" 
            for cmd in [["init"], ["validate"], ["plan"], ["apply", "-auto-approve"]]:
                if not self.run_terraform_command(["terraform"] + cmd, aws_env):
                    return False
            return True
        except Exception as e:
            print(f"❌ Deployment failed: {e}")
            self.message += f"❌ Deployment failed: {e}" + "\n"
            return False
        finally:
            os.chdir("..")

    def destroy_terraform(self):
        try:
            os.chdir("terraform_workspace")
            self.run_terraform_command(["terraform", "destroy", "-auto-approve"])
        except Exception as e:
            print(f"❌ Destruction failed: {e}")
        finally:
            os.chdir("..")



class RunTerraformView(TemplateView):
    template_name = "terraform.html"
    def get(self, request):
        return render(request, self.template_name)


class DetailsView(TemplateView):
    template_name = "detailsAws.html"
    def get(self, request):
        return render(request, self.template_name)

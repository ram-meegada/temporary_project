import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.generic.websocket import SyncConsumer
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


class BasicSyncConsumer(SyncConsumer):
    def websocket_connect(self, event):
        self.send({
            "type": "websocket.accept"
        })

    def websocket_receive(self, event):
        self.aws_env = {
            "AWS_ACCESS_KEY_ID": "AKIAYKFQQ6SE3FQ34QCZ",
            "AWS_SECRET_ACCESS_KEY": "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",
            "AWS_DEFAULT_REGION": "us-east-1",
            "AWS_DEFAULT_OUTPUT": "json"
        }

        self.errors = False
        whole_input = event.get('text', None)
        self.input = json.loads(whole_input)["message"]
        print(self.input, '---------event-----------')

        if self.input == "Destroy":
            self.send({
                    "type": "websocket.send",
                    "text": json.dumps({"temp": f"Destruction process started....", "type": 1})
                })
            self.destroy_terraform()
        else:
            if self.input:
                self.send({
                    "type": "websocket.send",
                    "text": json.dumps({"temp": f"Process Started....", "type": 1})
                })
            self.run()
            if not self.errors:
                self.get_recommendations(self.input)
        
    def run(self):
        try:
            prompt = self.input

            model = genai.GenerativeModel("gemini-1.5-pro-latest")
            response = model.generate_content(f"""
            You are an expert in Terraform and Infrastructure as Code.
            Generate valid Terraform code inside triple backticks (```hcl ... ```).
            Do not include any explanations, comments, or extra text.
            Include a provider block. Just return the Terraform code.
            Use string interpolation with ${{}} instead of using + directly in resource
            arn. In provider block use terraform version as 4.0 not more than that. Do not include required version of terrform in code.
            Request: {prompt}
            """)

            response_text = response.text if hasattr(response, 'text') else response.parts[0].text
            match = re.search(r"```(?:hcl)?\n(.*?)\n```", response_text, re.DOTALL)
            if match:
                terraform_code = match.group(1).strip()
            else:
                terraform_code = response_text.strip()
            
            self.run_terraform(terraform_code)
            # clean_message = re.sub(r'\x1b\[[0-9;]*m', '', self.message)
            self.send({
                "type": "websocket.send",
                "text": json.dumps({"temp": "Process Ended.", "type": 1}),
            })
        except Exception as err:
            self.errors = True
            self.send({
                "type": "websocket.send",
                "text": json.dumps({"temp": str(err), "type": 1})
            })

    # Terraform Execution Functions
    def run_terraform_command(self, command, aws_env):
        try:
            result = subprocess.run(command, check=True, capture_output=True, text=True, env={**os.environ, **aws_env} )
            success_msg = f"✅ {' '.join(command)} succeeded!\n{result.stdout}"
            print(success_msg)
            self.send({
                "type": "websocket.send",
                "text": json.dumps({"temp": self.strip_ansi_codes(success_msg), "type": 1})
            })
            return True
        except subprocess.CalledProcessError as e:
            self.errors = True
            error_msg = f"❌ Error: {' '.join(command)}\n{e.stderr}"
            print(error_msg)
            self.send({
                "type": "websocket.send",
                "text": json.dumps({"temp": self.strip_ansi_codes(error_msg), "type": 1})
                
            })
            return False

    def run_terraform(self, terraform_code):
        try:
            os.makedirs("terraform_workspace", exist_ok=True)
            os.chdir("terraform_workspace")
            with open("main.tf", "w") as f:
                f.write(terraform_code)

            print("✅ Code written to main.tf")
            self.send({
                "type": "websocket.send",
                "text": json.dumps({"temp": self.strip_ansi_codes("✅ Code written to main.tf"), "type": 1})
            }) 
            for cmd in [["init"], ["validate"], ["plan"], ["apply", "-auto-approve"]]:
                if not self.run_terraform_command(["terraform"] + cmd, self.aws_env):
                    return False
            return True
        except Exception as e:
            self.errors = True
            print(f"❌ Deployment failed: {e}")
            self.send({
                "type": "websocket.send",
                "text": json.dumps({"temp": self.strip_ansi_codes("❌ Deployment failed: {e}"), "type": 1})
            }) 
            return False
        finally:
            os.chdir("..")

    def get_recommendations(self, prompt):
        model = genai.GenerativeModel("gemini-1.5-pro-latest")
        response = model.generate_content(f"""
        A user deployed this Terraform service: \"\"\"{prompt}\"\"\"
        Provide exactly 4 enhancements (optimization, security, performance, usability).
        Use only hyphen bullets. Format: "- <recommendation>"
        No explanations or extra text. 
        Use string interpolation with ${{}} instead of using + directly in resource
            arn. In provider block use terraform version as 4.0 not more than that. Do not include required version of terrform in code.
        """)

        response_text = response.text if hasattr(response, 'text') else response.parts[0].text
        recommendations = re.findall(r'-\s*(.+?)\s*$', response_text, re.MULTILINE)
        if recommendations:
            self.send({
                "type": "websocket.send",
                "text": json.dumps({"temp": recommendations[:4], "type": 2})
            })
        else:
            self.send({
                "type": "websocket.send",
                "text": json.dumps({"temp": self.strip_ansi_codes("⚠️ No recommendations available"), "type": 1})
            })

    def strip_ansi_codes(self, s):
        return re.sub(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])', '', s)

    def websocket_disconnect(self, event):
        pass

    def destroy_terraform(self):
        try:
            os.chdir("terraform_workspace")
            self.run_terraform_command(["terraform", "destroy", "-auto-approve"], self.aws_env)
        except Exception as e:
            print(f"❌ Destruction failed: {e}")
            self.send({
                "type": "websocket.send",
                "text": json.dumps({"temp": self.strip_ansi_codes(f"❌ Destruction failed: {e}"), "type": 1})
            })
        finally:
            os.chdir("..")




class DetailsConsumer(SyncConsumer):
    def websocket_connect(self, event):
        self.send({
            "type": "websocket.accept"
        })

    def websocket_receive(self, event):
        self.aws_env = {
            "AWS_ACCESS_KEY_ID": "AKIAYKFQQ6SE3FQ34QCZ",
            "AWS_SECRET_ACCESS_KEY": "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",
            "AWS_DEFAULT_REGION": "us-east-1",
            "AWS_DEFAULT_OUTPUT": "json"
        }
        message = event.get('text', None)
        self.input = json.loads(message)["message"]
        if message:
            print(f"Received message: {self.input}")

        tf_code = self.generate_generic_output_code(self.input)

        print("✅ Generated Code:\n", tf_code)
        self.send({
                "type": "websocket.send",
                "text": json.dumps({"temp": self.strip_ansi_codes(f"✅ Generated Code:\n, {tf_code}")})
            })
        # Check if it's a data block
        if tf_code:
            is_data_block = bool(re.search(r'data\s+"([^"]+)"\s+"([^"]+)"', tf_code))

            # Extract Terraform resource/data address
            match = re.search(r'(resource|data)\s+"([^"]+)"\s+"([^"]+)"', tf_code)
            id_match = re.search(r'bucket\s*=\s*"([^"]+)"|instance_id\s*=\s*"([^"]+)"|id\s*=\s*"([^"]+)"', tf_code)

            if not match:
                print("❌ Could not extract Terraform resource/data block.")
                self.send({
                    "type": "websocket.send",
                    "text": json.dumps({"temp": self.strip_ansi_codes("❌ Could not extract Terraform resource/data block.")})
                })
                return

            resource_type = match.group(2)
            resource_name = match.group(3)
            resource_address = f"{resource_type}.{resource_name}" if match.group(1) == "resource" else None

            import_id = next((i for i in id_match.groups() if i), None) if id_match else None

            if not import_id and not is_data_block:
                print("❌ Could not auto-extract import ID. Please include resource ID in your prompt.")
                self.send({
                    "type": "websocket.send",
                    "text": json.dumps({"temp": self.strip_ansi_codes("❌ Could not auto-extract import ID. Please include resource ID in your prompt.")})
                })
                return

            print(f"📦 Proceeding with: {'data' if is_data_block else 'resource'} block")
            self.send({
                    "type": "websocket.send",
                    "text": json.dumps({"temp": self.strip_ansi_codes(f"📦 Proceeding with: {'data' if is_data_block else 'resource'} block")})
                })
            self.run_import_flow(tf_code, import_id, resource_address, is_data_block=is_data_block)
        else:
            self.send({
                    "type": "websocket.send",
                    "text": json.dumps({"temp": self.strip_ansi_codes(f"Unable to generate terraform code.")})
                })

    # Function to generate Terraform code for any AWS service
    def generate_generic_output_code(self, prompt):
        model = genai.GenerativeModel("gemini-1.5-pro-latest")
        response = model.generate_content(f"""
        Generate valid Terraform code inside triple backticks (```hcl ... ```).
        Use only a resource block and a corresponding output block to extract requested details.
        Do NOT use any data blocks.

        Always include a valid `provider "aws"` block with the correct region **outside** of the resource block.
        Do NOT place `region` inside the resource itself.

        If the prompt asks for website hosting, use `website` block inside `aws_s3_bucket` (not `aws_s3_bucket_website_configuration`).
        Ensure you include required fields like `index_document` and `error_document`and don't write acl line in the resource block.

        Prompt: {prompt}
        """)

        response_text = getattr(response, 'text', response.parts[0].text if hasattr(response, 'parts') else "")
        match = re.search(r"```(?:hcl)?(.*?)```", response_text, re.DOTALL)
        if match:
            return match.group(1).strip()
        else:
            return response_text.strip()

    # Execute Terraform flow: write, init, import (if needed), apply
    def run_import_flow(self, terraform_code, import_id, resource_address, is_data_block=False):
        try:
            os.makedirs("terraform_workspace", exist_ok=True)
            os.chdir("terraform_workspace")

            with open("main.tf", "w") as f:
                f.write(terraform_code)

            print("✅ Terraform code written.")
            self.send({
                    "type": "websocket.send",
                    "text": json.dumps({"temp": self.strip_ansi_codes("✅ Terraform code written.")})
                })
            if not self.run_terraform_command(["terraform", "init"], self.aws_env): return False

            # Only import if it's a resource block
            if not is_data_block and resource_address and import_id:
                print(f"📥 Importing resource: {resource_address} -> {import_id}")
                self.send({
                    "type": "websocket.send",
                    "text": json.dumps({"temp": self.strip_ansi_codes(f"📥 Importing resource: {resource_address} -> {import_id}")})
                })
                if not self.run_terraform_command(["terraform", "import", resource_address, import_id], self.aws_env): return False

            print("🚀 Running Terraform apply to fetch output...")
            self.send({
                    "type": "websocket.send",
                    "text": json.dumps({"temp": self.strip_ansi_codes("🚀 Running Terraform apply to fetch output...")})
                })
            if not self.run_terraform_command(["terraform", "apply", "-auto-approve"], self.aws_env): return False

            print("✅ Terraform applied. Outputs below:")
            self.send({
                    "type": "websocket.send",
                    "text": json.dumps({"temp": self.strip_ansi_codes("✅ Terraform applied. Outputs below:")})
                })
            self.run_terraform_command(["terraform", "output"], self.aws_env)
            return True

        except Exception as e:
            print(f"❌ Error: {e}")
            self.send({
                    "type": "websocket.send",
                    "text": json.dumps({"temp": self.strip_ansi_codes(f"❌ Error: {e}")})
                })
            return False

    # Run a Terraform CLI command
    def run_terraform_command(self, command, aws_env):
        try:
            result = subprocess.run(command, check=True, capture_output=True, text=True, env={**os.environ, **aws_env})
            print(result.stdout)
            self.send({
                    "type": "websocket.send",
                    "text": json.dumps({"temp": self.strip_ansi_codes(result.stdout)})
                })
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ {e.stderr}")
            self.send({
                    "type": "websocket.send",
                    "text": json.dumps({"temp": self.strip_ansi_codes(f"❌ {e.stderr}")})
                })
            return False

    def strip_ansi_codes(self, s):
        return re.sub(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])', '', s)

    def websocket_disconnect(self, event):
        print("WebSocket disconnected")

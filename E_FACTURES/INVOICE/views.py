from django.shortcuts import render
from rest_framework import viewsets
from .models import facture as Efacture
from .serializers import FactureSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from django.core.files.storage import default_storage
from django.conf import settings
from django.apps import apps
from ollama import chat
from PIL import Image
import pytesseract
import os,json,csv
from datetime import datetime
from rest_framework import status
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
from transformers import CamembertTokenizer, CamembertForSequenceClassification

# cvs_path='C:/Users/hp/Desktop/phi2/efacture/plan.csv'
# model_directory = "D:/huggingface_cache/hub/models--microsoft--phi-2/snapshots/ef382358ec9e382308935a992d908de099b64c23"
# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# # === CHARGEMENT UNIQUE (à faire une seule fois au démarrage)
# tokenizer = AutoTokenizer.from_pretrained(model_directory, local_files_only=True)
# model = AutoModelForCausalLM.from_pretrained(model_directory, local_files_only=True, torch_dtype="auto").to(device)

# if tokenizer.pad_token is None:
#     tokenizer.pad_token = tokenizer.eos_token

# Create your views here.
def home(request):
    user_=request.user
    return render(request,
                  'invoice/facture.html',
                  {'user_': user_.username})
    

class FactureViewSet(viewsets.ModelViewSet):
    queryset = Efacture.objects.all()
    serializer_class = FactureSerializer
    print(serializer_class)
    

# class FileUploadView(APIView):
#     parser_classes = [MultiPartParser]

#     def post(self, request, *args, **kwargs):
#         if 'file' not in request.data:
#             return Response({'error': 'No file provided'}, status=400)

#         file_obj = request.data['file']
#         filename = default_storage.save(file_obj.name, file_obj)
        
#         return Response({
#             'message': 'Fichier uploadé avec succès',
#             'file_url': request.build_absolute_uri(settings.MEDIA_URL + filename)
#         })

# class FileUploadView(APIView):
#     parser_classes = [MultiPartParser]

#     def post(self, request):
#         if 'file' not in request.data:
#             return Response({'error': 'No file provided'}, status=400)

#         # 1. Save file
#         file_obj = request.data['file']
#         print(file_obj)
#         filename = default_storage.save(file_obj.name, file_obj)
#         filepath = os.path.join(settings.MEDIA_ROOT, filename)
#         print('ocr') 
#         # 2. OCR
#         try:
            
#             text = pytesseract.image_to_string(Image.open(filepath))
           
#         except Exception as e:
#             return Response({'error': 'OCR failed', 'detail': str(e)}, status=500)

#         # 3. Prompt pour extraction LLM
#         system_prompt = """Tu es un assistant d'extraction de données de factures.
# Retourne un JSON avec les champs suivants si présents :
# - numFacture
# - datefacture
# - total
# - categorieFacture
# Extrait uniquement les données, pas d'explication.
# Format : JSON.
# """
#         user_input = f"Voici le texte extrait d'une facture :\n{text}"
    
#         try:
#             response = chat(
#                 model='mistral',  # ou llama3, mixtral, etc.
#                 messages=[
#                     {"role": "system", "content": system_prompt},
#                     {"role": "user", "content": user_input}
#                 ]
#             )
#             print(response)
#             return Response(response['message']['content'])  # contient le JSON
#         except Exception as e:
#             return Response({'error': 'LLM failed', 'detail': str(e)}, status=500)

def csv_to_json_string(csv_file_path):
    result = []
    with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
        # print(csvfile)
        reader = csv.DictReader(csvfile)
        for row in reader:
            compte = row.get('compte') 
            libelle = row.get('categorie') 
            if compte and libelle:
                result.append({"compte": compte.strip(), "categorie": libelle.strip()})
    return json.dumps(result, ensure_ascii=False, indent=2)
# plan_flat=csv_to_json_string(cvs_path)

id2label={0: 4451, 1: 104000, 2: 131000, 3: 165000, 4: 203000, 5: 207000, 6: 261000, 7: 270000, 8: 442100, 9: 455000, 10: 467000, 11: 531000, 12: 601000, 13: 602000, 14: 604000, 15: 606400, 16: 607000, 17: 613200, 18: 621000, 19: 622000, 20: 623000, 21: 624100, 22: 625000, 23: 625110, 24: 625200, 25: 625400, 26: 626000, 27: 631300, 28: 641000, 29: 645000, 30: 647000, 31: 654000, 32: 666000, 33: 671000, 34: 681000, 35: 701000, 36: 707000, 37: 756000, 38: 760000, 39: 770000, 40: 790000}

class IdentiferView(APIView):
    def post(self, request):
        try:
            facture=request.data
            categ=facture.get('categ')
            print(categ) 
            model_path = "modele_comptable"
            tokenizer = CamembertTokenizer.from_pretrained(model_path)
            model = CamembertForSequenceClassification.from_pretrained(model_path)
            # text='VENTE DE PRODUITS'
            inputs = tokenizer(categ, return_tensors="pt", padding=True, truncation=True)
            with torch.no_grad():
                outputs = model(**inputs)
                
            # Get prediction
            logits = outputs.logits
            predicted_class_id = torch.argmax(logits, dim=1).item()

            # Map back to account number
            predicted_account = id2label[predicted_class_id]
            print(f"Texte : {categ}")
            print(f"Compte comptable prédit : {predicted_account}")
            # test
            # texte_facture = f"""
            
            # Détails Facture : {facture.get('categ')}
            # """
            # texte_facture = f"""Facture n° {facture.get('num')} 
            # Date : {facture.get('datefact')}
            # Montant : {facture.get('total')} €
            # Détails : {facture.get('categ')}
            # """
            #texte_facture="details facture:"+facture.get('categ')
            # compte = classify_invoice_text(texte_facture)
            fact=Efacture.objects.filter(num=facture.get('num')).first()
            if fact:
                fact.compte=predicted_account
                fact.save()
                return Response(1)
            else:
                return Response(0)
        except Exception as e:
            return Response({"error": "Failed to fetch comptes", "detail": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# def classify_invoice_text(texte_facture: str):
#     #print(plan_flat)
    
#     prompt = f"""Voici une facture. Ta tâche est de prédire uniquement les catégories applicables à partir de la liste suivante, séparées par des points-virgules : 

# Maintenance informatique; Frais de réception clients; Amortissement matériel; Honoraires juridiques; Dotations aux provisions; Assurance; Abonnement; Frais internet; Autres.

# Facture :
# {texte_facture}

# Catégories (répond uniquement avec des catégories parmi la liste) :"""

# # === TOKENISATION ET GÉNÉRATION ===
#     inputs = tokenizer(prompt, return_tensors="pt", padding=True, truncation=True, max_length=256)
#     inputs = {k: v.to(device) for k, v in inputs.items()}

#     print("🕒 Génération en cours...")
#     outputs = model.generate(
#         input_ids=inputs["input_ids"],
#         attention_mask=inputs["attention_mask"],
#         max_new_tokens=50,
#         do_sample=True,
#         pad_token_id=tokenizer.pad_token_id
#     )
#     print("✅ Génération terminée.")

#     # === DÉCODAGE ET AFFICHAGE ===
#     predicted_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
#     print("📤 Réponse brute :")
#     print(predicted_text)

#     # === EXTRACTION DES CATÉGORIES ===
#     for line in predicted_text.splitlines():
#         if "Catégories" in line:
#             print("🏷️  Catégories détectées :", line.split(":")[-1].strip())
#             break
#     else:
#         print("❌ Aucune catégorie détectée.")
#     return []
from django.db.models import Sum,Count

class DashView(APIView):
    def post(self,request):
        factures=Efacture.objects.all()
        totaux = factures.aggregate(
            total_tva=Sum('tva'),
            total_ttc=Sum('total')
        )
        # Nettoyage/formatage (facultatif)
        total_tva = totaux.get('total_tva') or 0
        total_ttc = totaux.get('total_ttc') or 0
        facture_stats = factures.values('categ').annotate(count=Count('id')).order_by('categ')
        return Response({'totaux':{
            'total_tva': round(total_tva, 2),
            'total_ttc': round(total_ttc, 2),
            'nbr_fact':len(factures),
            'data1':self.getData1(factures),
            'data2':list(facture_stats)
        }})
    def getData1(self,facts):
        result=[]
        print(facts)
        for r in facts:
            result.append({
                'date':str(r.datefact),
                'ttc':r.total,
                'tva':r.tva
            })
        return result
class FileUploadView(APIView):
    def post(self, request):
        if 'file' not in request.data:
            return Response({'error': 'No file provided'}, status=400)

        # Save the file
        file_obj = request.data['file']
        filename = default_storage.save(file_obj.name, file_obj)
        filepath = os.path.join(settings.MEDIA_ROOT, filename)

        # Perform OCR
        try:
            text = pytesseract.image_to_string(Image.open(filepath))
        except Exception as e:
            return Response({'error': 'OCR failed', 'detail': str(e)}, status=500)

        system_prompt = """Tu es un assistant d'extraction de données de factures.
Retourne un JSON avec les champs suivants si présents :
- numFacture
- dateFacture
- Total
- categorieFacture
-Tva
Extrait uniquement les données, pas d'explication.
Format : JSON.
"""
        user_input = f"Voici le texte extrait d'une facture :\n{text}"
        print(user_input)
        try:
            # Access the preloaded callable from the app config
            app_config = apps.get_app_config('invoice')
            model_callable = app_config.ollama_model

            response = model_callable(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_input}
                ]
            )
            # Extract content string and parse it as JSON
            content = response['message']['content']
            print("Raw content from model:", content)

            parsed_json = json.loads(content)
            raw_date = parsed_json.get('dateFacture')
            datefact=None
            try:
                # Convert 'DD/MM/YYYY' to 'YYYY-MM-DD'
                datefact = datetime.strptime(raw_date, "%d/%m/%Y").date()
            except (ValueError, TypeError):
                datefact=None
                # return Response({'error': 'Invalid date format in facture'}, status=400)
            var = {
                'num': parsed_json.get('numFacture'),
                'datefact': datefact,
                'total': parsed_json.get('Total'),
                'tva': parsed_json.get('Tva'),
                'categ': parsed_json.get('categorieFacture'),
                'textfact':text,
                'path':filename
            }

            # Assuming `facture` is already imported and fields match the keys in `var`
            fact=Efacture.objects.create(**var)
            if fact:
                
                return Response(fact.id)
            else:
                return Response(None)
        except Exception as e:
            return Response({'error': 'LLM failed', 'detail': str(e)}, status=500)
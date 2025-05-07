
### 5. **5_Association_Compte_Comptable.rst**

#### Objectif :
Expliquer le processus d'association des informations extraites aux comptes comptables.

```rst
# Association au Compte Comptable

## Objectifs de l'Association
L'objectif principal de cette étape est d'associer chaque élément extrait d'une facture (comme le montant ou le type de bien/service) à un compte comptable spécifique. Cela garantit que les informations extraites sont correctement classées pour une gestion comptable optimale.

### Méthodes d'association
1. **Règles métiers** : Nous avons défini des règles simples pour associer certains types d'informations extraites à des comptes comptables. Par exemple, un montant relatif à une vente de biens sera associé à un compte "Ventes".
2. **Apprentissage supervisé** : Dans les cas plus complexes, nous utilisons un modèle d'apprentissage supervisé pour prédire le compte comptable à partir des informations extraites.
3. **Validation** : Une fois l'association effectuée, nous vérifions la précision des résultats en comparant les associations faites par le modèle avec celles réalisées manuellement.

### Exemple de code pour l'association
```python
# Exemple de règles pour l'association
def associer_compte(montant, categorie):
    if categorie == 'Vente':
        return '701', montant
    elif categorie == 'Achat':
        return '607', montant
    else:
        return 'Autre', montant

# Application de l'association sur un exemple
compte, montant = associer_compte(1000, 'Vente')
print(f"Compte associé : {compte}, Montant : {montant}")





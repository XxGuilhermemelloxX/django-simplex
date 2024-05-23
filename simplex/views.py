# simplex_app/views.py
from django.shortcuts import render
from .simplex_app import simplex


def simplex_view(request):
    context = {}
    if request.method == 'POST':
        try:
            # Processa os coeficientes da função objetivo
            c = list(map(float, request.POST.get('c').split(',')))

            A_ub = []
            b_ub = []
            A_eq = []
            b_eq = []

            # Processa as restrições
            inequalities = request.POST.get('inequalities').split(';')
            for ineq in inequalities:
                parts = ineq.split(',')
                row = list(map(float, parts[:-2]))
                sign = parts[-2]
                value = float(parts[-1])

                if sign == '<=':
                    A_ub.append(row)
                    b_ub.append(value)
                elif sign == '>=':
                    A_ub.append([-1 * x for x in row])
                    b_ub.append(-1 * value)
                elif sign == '=':
                    A_eq.append(row)
                    b_eq.append(value)

            maximize = 'maximize' in request.POST and request.POST.get('maximize') == 'on'

            # Verifica se A_ub tem duas dimensões e se as colunas de A_ub são iguais ao tamanho de c
            if A_ub and len(A_ub[0]) != len(c):
                context[
                    'error'] = "A matriz de coeficientes de desigualdade (A_ub) deve ter exatamente duas dimensões, e o número de colunas em A_ub deve ser igual ao tamanho de c."
            else:
                result = simplex(c, A_ub, b_ub, A_eq if A_eq else None, b_eq if b_eq else None, maximize=maximize)
                context['result'] = result
        except ValueError as e:
            context['error'] = f"Por favor, insira valores numéricos válidos nos campos. Erro: {str(e)}"

    return render(request, 'simplex.html', context)

import matplotlib
matplotlib.use('TkAgg')
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import TextBox, Button
import sympy as sp

plt.rcParams['toolbar'] = 'None'

class FunctionPlotter:
    def __init__(self):
        self.fig, self.ax = plt.subplots(figsize=(12, 8))
        plt.subplots_adjust(bottom=0.3)
        
        # Fonction par défaut
        self.function_str = "x**2 - 4*x + 3"
        self.x_min = -10
        self.x_max = 10
        self.y_min = -10
        self.y_max = 10
        
        # Désactiver complètement les coordonnées au survol
        self.fig.canvas.toolbar = None
        
        # Création de l'interface
        self.create_widgets()
        self.plot_function()
        
    def create_widgets(self):
        ax_func = plt.axes([0.15, 0.15, 0.7, 0.05])
        self.text_func = TextBox(ax_func, 'f(x) = ', initial=self.function_str)
        self.text_func.on_submit(self.update_function)
        
        ax_xmin = plt.axes([0.15, 0.08, 0.15, 0.05])
        self.text_xmin = TextBox(ax_xmin, 'x min: ', initial=str(self.x_min))
        self.text_xmin.on_submit(self.update_range)
        
        ax_xmax = plt.axes([0.45, 0.08, 0.15, 0.05])
        self.text_xmax = TextBox(ax_xmax, 'x max: ', initial=str(self.x_max))
        self.text_xmax.on_submit(self.update_range)
        
        # Zone pour y_min
        ax_ymin = plt.axes([0.15, 0.01, 0.15, 0.05])
        self.text_ymin = TextBox(ax_ymin, 'y min: ', initial=str(self.y_min))
        self.text_ymin.on_submit(self.update_range)
        
        # Zone pour y_max
        ax_ymax = plt.axes([0.45, 0.01, 0.15, 0.05])
        self.text_ymax = TextBox(ax_ymax, 'y max: ', initial=str(self.y_max))
        self.text_ymax.on_submit(self.update_range)
        
        # Bouton pour tracer
        ax_button = plt.axes([0.7, 0.08, 0.15, 0.05])
        self.btn_plot = Button(ax_button, 'Tracer')
        self.btn_plot.on_clicked(self.plot_function)
        
        # Crédit en bas à droite de la fenêtre
        ax_credit = plt.axes([0.7, 0.01, 0.28, 0.03])
        ax_credit.axis('off')
        ax_credit.text(1, 0.5, 'Created by Mehdi Talalha', 
                      ha='right', va='center',
                      fontsize=10, weight='bold')
        
    def safe_eval(self, expr_str, x_val):
        """Évaluation sécurisée d'une expression mathématique"""
        try:
            x = sp.Symbol('x')
            expr = sp.sympify(expr_str)
            f = sp.lambdify(x, expr, modules=['numpy'])
            return f(x_val)
        except Exception as e:
            print(f"Erreur: {e}")
            return None
    
    def plot_function(self, event=None):
        """Trace la fonction"""
        self.ax.clear()
        
        try:
            # Générer les points avec plus de précision
            x = np.linspace(self.x_min, self.x_max, 2000)
            y = self.safe_eval(self.function_str, x)
            
            if y is None:
                self.ax.text(0.5, 0.5, 'Erreur dans la fonction!', 
                           ha='center', va='center', transform=self.ax.transAxes,
                           fontsize=14, color='red')
                plt.draw()
                return
            
            # Tracer la fonction
            self.ax.plot(x, y, 'b-', linewidth=2, label=f'f(x) = {self.function_str}')
            
            # Axes et grille - toujours visibles
            self.ax.axhline(y=0, color='k', linewidth=1.5)
            self.ax.axvline(x=0, color='k', linewidth=1.5)
            self.ax.grid(True, alpha=0.3)
            
            # Fixer l'intervalle Y pour garder l'échelle constante (vecteur j = 1)
            self.ax.set_ylim(self.y_min, self.y_max)
            
            # Afficher les graduations sur tous les côtés
            self.ax.tick_params(axis='both', which='both', 
                              bottom=True, top=True, 
                              left=True, right=True,
                              labelbottom=True, labeltop=False,
                              labelleft=True, labelright=False)
            
            # Désactiver complètement l'affichage des coordonnées
            self.ax.format_coord = lambda x, y: ''
            
            # Labels et titre
            self.ax.set_xlabel('x', fontsize=12)
            self.ax.set_ylabel('y', fontsize=12)
            self.ax.set_title('Représentation graphique de la fonction', fontsize=14, fontweight='bold')
            self.ax.legend(loc='best')
            
            # Trouver et marquer les racines (sans annotations)
            try:
                y_array = np.array(y)
                sign_changes = np.where(np.diff(np.sign(y_array)))[0]
                
                # Calculer les racines exactes avec sympy si possible
                x_sym = sp.Symbol('x')
                expr = sp.sympify(self.function_str)
                roots = sp.solve(expr, x_sym)
                
                # Filtrer les racines réelles dans l'intervalle
                real_roots = []
                for root in roots:
                    if root.is_real:
                        root_val = float(root.evalf())
                        if self.x_min <= root_val <= self.x_max:
                            real_roots.append(root_val)
                            self.ax.plot(root_val, 0, 'go', markersize=10)
                
            except Exception as e:
                # Si le calcul exact échoue, utiliser l'approximation
                for idx in sign_changes[:5]:
                    root_x = x[idx]
                    self.ax.plot(root_x, 0, 'go', markersize=10)
            
            plt.draw()
            
        except Exception as e:
            print(f"Erreur lors du tracé: {e}")
            self.ax.text(0.5, 0.5, f'Erreur: {str(e)}', 
                       ha='center', va='center', transform=self.ax.transAxes,
                       fontsize=12, color='red')
            plt.draw()
    
    def update_function(self, text):
        """Met à jour la fonction"""
        self.function_str = text
        self.plot_function()
    
    def update_range(self, text):
        """Met à jour l'intervalle"""
        try:
            self.x_min = float(self.text_xmin.text)
            self.x_max = float(self.text_xmax.text)
            self.y_min = float(self.text_ymin.text)
            self.y_max = float(self.text_ymax.text)
            self.plot_function()
        except ValueError:
            print("Erreur: valeurs invalides pour l'intervalle")


def main():
    """Fonction principale"""
    print("=" * 60)
    print("TRACEUR DE FONCTIONS NUMÉRIQUES")
    print("=" * 60)
    print("\nExemples de fonctions à essayer:")
    print("  - Polynômes: x**2 - 4*x + 3, x**3 - 3*x")
    print("  - Trigonométriques: sin(x), cos(x), tan(x)")
    print("  - Exponentielles: exp(x), 2**x")
    print("  - Logarithmes: log(x), log(x**2 + 1)")
    print("  - Rationnelles: 1/x, (x**2 - 1)/(x + 2)")
    print("  - Racines: sqrt(x), sqrt(x**2 + 1)")
    print("\nSyntaxe:")
    print("  - Puissance: x**2 ou x^2")
    print("  - Multiplication: 2*x (le * est obligatoire)")
    print("  - Pi: pi")
    print("  - Exponentielle: exp(x) ou E**x")
    print("\nModifiez la fonction et l'intervalle dans l'interface graphique!")
    print("=" * 60)
    
    try:
        plotter = FunctionPlotter()
        plt.show()
    except ImportError as e:
        print(f"\nERREUR: Bibliothèque manquante - {e}")
        print("\nInstallez les dépendances avec:")
        print("  pip install numpy matplotlib sympy")


if __name__ == "__main__":
    main()


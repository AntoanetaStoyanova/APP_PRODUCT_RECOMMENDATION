import psycopg2



POSTGRESQL_URI = 'postgresql://postgres:Kandinsky_95@localhost:5432/postgres'


# afficher les produits selon le goût choisit
def get_products(gout, per_page, offset):
    """Récupère les produits depuis la base de données."""
    connection = psycopg2.connect(POSTGRESQL_URI)
    produits_list = []
    total_count = 0

    with connection:
        with connection.cursor() as cursor:
            cursor.execute(
                'SELECT id_produit, img_produit, nom_produit FROM public.produits WHERE gout = %s LIMIT %s OFFSET %s;',
                (gout, per_page, offset)
            )
            produits_list = cursor.fetchall()

            cursor.execute(
                'SELECT COUNT(*) FROM public.produits WHERE gout = %s;',
                (gout,)
            )
            total_count = cursor.fetchone()[0]

    return produits_list, total_count



# produits affichés à partir la recommendation embedding
def get_user_products(user_id):
    """Récupère les produits associés à un utilisateur spécifique."""
    connection = psycopg2.connect(POSTGRESQL_URI)
    produits_list = []

    with connection:
        with connection.cursor() as cursor:
            cursor.execute(
                '''SELECT p.img_produit, p.nom_produit
                   FROM public.produits p
                   JOIN public.user_produit up ON p.id_produit = up.product_id
                   WHERE up.user_id = %s;''',
                (user_id,)
            )
            produits_list = cursor.fetchall()

    return produits_list

# produits affichés à partir la recommendation llm
def show_produit(id_produit_list):
    """Récupère les images des produits à partir de leurs ID en base de données."""
    if not id_produit_list:
        return ["Aucune image disponible pour ce produit"]

    img_produit_values = []

    connection = psycopg2.connect(POSTGRESQL_URI)
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(
                '''SELECT img_produit, nom_produit
                   FROM public.produits
                   WHERE id_produit = ANY(%s);''',
                (id_produit_list,)
            )
            img_produit_values = [row[0] for row in cursor.fetchall()]

    # Si aucune image n'est trouvée, renvoyer un message par défaut
    if not img_produit_values:
        img_produit_values = ["Aucune image disponible pour ce produit"] * len(id_produit_list)

    return img_produit_values
# TIPE (French)

Ce projet est mon TIPE de classe préparatoire MP, présenté en 2015.

Il implémente l'algorithme de sélection de points d'intérêts dans une vidéo et de calcul du mouvement des objets, développé par Lucas, Kanade, Tomasi (points KLT).
Le programme présenté prends en entrée deux images supposées proche temporellement dans une vidéo, et est capable de :
- générer une version altérée présentant les points d'intérêts (divers seuils d'intérêts en divers couleurs, réglable)
- créer une image dont la valeur d'intensité lumineuse représente l'intérêt du point
- calculer le mouvement qu'il y a eu entre les deux images (en supposant que l'image entière soit un unique objet)

Ce TIPE a reçu la note de 20/20.

Pour plus d'informations sur les fondements mathématiques de l'algorithme, voir : https://en.wikipedia.org/wiki/Kanade%E2%80%93Lucas%E2%80%93Tomasi_feature_tracker

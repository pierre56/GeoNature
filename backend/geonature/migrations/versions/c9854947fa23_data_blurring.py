"""data blurring

Revision ID: c9854947fa23
Revises: 3b2f3de760dc
Create Date: 2021-10-11 16:24:28.933191

"""
import importlib

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c9854947fa23'
down_revision = '3b2f3de760dc'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("""
    DROP VIEW gn_synthese.v_synthese_for_export;
    CREATE VIEW gn_synthese.v_synthese_for_export AS
        SELECT
            s.id_synthese AS id_synthese,
            s.date_min::date AS date_debut,
            s.date_max::date AS date_fin,
            s.date_min::time AS heure_debut,
            s.date_max::time AS heure_fin,
            t.cd_nom AS cd_nom,
            t.cd_ref AS cd_ref,
            t.nom_valide AS nom_valide,
            t.nom_vern AS nom_vernaculaire,
            s.nom_cite AS nom_cite,
            t.regne AS regne,
            t.group1_inpn AS group1_inpn,
            t.group2_inpn AS group2_inpn,
            t.classe AS classe,
            t.ordre AS ordre,
            t.famille AS famille,
            t.id_rang AS rang_taxo,
            s.count_min AS nombre_min,
            s.count_max AS nombre_max,
            s.altitude_min AS alti_min,
            s.altitude_max AS alti_max,
            s.depth_min AS prof_min,
            s.depth_max AS prof_max,
            s.observers AS observateurs,
            s.id_digitiser AS id_digitiser, -- Utile pour le CRUVED
            s.determiner AS determinateur,
            communes AS communes,
            public.ST_astext(s.the_geom_4326) AS geometrie_wkt_4326,
            public.ST_x(s.the_geom_point) AS x_centroid_4326,
            public.ST_y(s.the_geom_point) AS y_centroid_4326,
            public.ST_asgeojson(s.the_geom_4326) AS geojson_4326,-- Utile pour la génération de l'export en SHP
            public.ST_asgeojson(s.the_geom_local) AS geojson_local,-- Utile pour la génération de l'export en SHP
            s.place_name AS nom_lieu,
            s.comment_context AS comment_releve,
            s.comment_description AS comment_occurrence,
            s.validator AS validateur,
            n21.label_default AS niveau_validation,
            s.meta_validation_date AS date_validation,
            s.validation_comment AS comment_validation,
            s.digital_proof AS preuve_numerique_url,
            s.non_digital_proof AS preuve_non_numerique,
            d.dataset_name AS jdd_nom,
            d.unique_dataset_id AS jdd_uuid,
            d.id_dataset AS jdd_id, -- Utile pour le CRUVED
            af.acquisition_framework_name AS ca_nom,
            af.unique_acquisition_framework_id AS ca_uuid,
            d.id_acquisition_framework AS ca_id,
            s.cd_hab AS cd_habref,
            hab.lb_code AS cd_habitat,
            hab.lb_hab_fr AS nom_habitat,
            s.precision AS precision_geographique,
            n1.label_default AS nature_objet_geo,
            n2.label_default AS type_regroupement,
            s.grp_method AS methode_regroupement,
            n3.label_default AS technique_observation,
            n5.label_default AS biologique_statut,
            n6.label_default AS etat_biologique,
            n22.label_default AS biogeographique_statut,
            n7.label_default AS naturalite,
            n8.label_default AS preuve_existante,
            n9.label_default AS niveau_precision_diffusion,
            n10.label_default AS stade_vie,
            n11.label_default AS sexe,
            n12.label_default AS objet_denombrement,
            n13.label_default AS type_denombrement,
            n14.label_default AS niveau_sensibilite,
            n15.label_default AS statut_observation,
            n16.label_default AS floutage_dee,
            n17.label_default AS statut_source,
            n18.label_default AS type_info_geo,
            n19.label_default AS methode_determination,
            n20.label_default AS comportement,
            s.reference_biblio AS reference_biblio,
            s.entity_source_pk_value AS id_origine,
            s.unique_id_sinp AS uuid_perm_sinp,
            s.unique_id_sinp_grp AS uuid_perm_grp_sinp,
            s.meta_create_date AS date_creation,
            s.meta_update_date AS date_modification,
            COALESCE(s.meta_update_date, s.meta_create_date) AS derniere_action,
            s.id_nomenclature_sensitivity,
            s.id_nomenclature_diffusion_level
        FROM gn_synthese.synthese AS s
            JOIN taxonomie.taxref AS t
                ON ( t.cd_nom = s.cd_nom )
            JOIN gn_meta.t_datasets AS d
                ON ( d.id_dataset = s.id_dataset )
            JOIN gn_meta.t_acquisition_frameworks AS af
                ON ( d.id_acquisition_framework = af.id_acquisition_framework )
            LEFT OUTER JOIN (
                    SELECT id_synthese, string_agg(DISTINCT area_name, ', ') AS communes
                    FROM gn_synthese.cor_area_synthese cas
                        LEFT OUTER JOIN ref_geo.l_areas a_1 ON cas.id_area = a_1.id_area
                        JOIN ref_geo.bib_areas_types ta ON ta.id_type = a_1.id_type AND ta.type_code ='COM'
                    GROUP BY id_synthese
                ) AS sa
                ON ( sa.id_synthese = s.id_synthese )
            LEFT JOIN ref_nomenclatures.t_nomenclatures AS n1
                ON ( s.id_nomenclature_geo_object_nature = n1.id_nomenclature )
            LEFT JOIN ref_nomenclatures.t_nomenclatures AS n2
                ON ( s.id_nomenclature_grp_typ = n2.id_nomenclature )
            LEFT JOIN ref_nomenclatures.t_nomenclatures AS n3
                ON ( s.id_nomenclature_obs_technique = n3.id_nomenclature )
            LEFT JOIN ref_nomenclatures.t_nomenclatures AS n5
                ON ( s.id_nomenclature_bio_status = n5.id_nomenclature )
            LEFT JOIN ref_nomenclatures.t_nomenclatures AS n6
                ON ( s.id_nomenclature_bio_condition = n6.id_nomenclature )
            LEFT JOIN ref_nomenclatures.t_nomenclatures AS n7
                ON ( s.id_nomenclature_naturalness = n7.id_nomenclature )
            LEFT JOIN ref_nomenclatures.t_nomenclatures AS n8
                ON ( s.id_nomenclature_exist_proof = n8.id_nomenclature )
            LEFT JOIN ref_nomenclatures.t_nomenclatures AS n9
                ON ( s.id_nomenclature_diffusion_level = n9.id_nomenclature )
            LEFT JOIN ref_nomenclatures.t_nomenclatures AS n10
                ON ( s.id_nomenclature_life_stage = n10.id_nomenclature )
            LEFT JOIN ref_nomenclatures.t_nomenclatures AS n11
                ON ( s.id_nomenclature_sex = n11.id_nomenclature )
            LEFT JOIN ref_nomenclatures.t_nomenclatures AS n12
                ON ( s.id_nomenclature_obj_count = n12.id_nomenclature )
            LEFT JOIN ref_nomenclatures.t_nomenclatures AS n13
                ON ( s.id_nomenclature_type_count = n13.id_nomenclature )
            LEFT JOIN ref_nomenclatures.t_nomenclatures AS n14
                ON ( s.id_nomenclature_sensitivity = n14.id_nomenclature )
            LEFT JOIN ref_nomenclatures.t_nomenclatures AS n15
                ON ( s.id_nomenclature_observation_status = n15.id_nomenclature )
            LEFT JOIN ref_nomenclatures.t_nomenclatures AS n16
                ON ( s.id_nomenclature_blurring = n16.id_nomenclature )
            LEFT JOIN ref_nomenclatures.t_nomenclatures AS n17
                ON ( s.id_nomenclature_source_status = n17.id_nomenclature )
            LEFT JOIN ref_nomenclatures.t_nomenclatures AS n18
                ON ( s.id_nomenclature_info_geo_type = n18.id_nomenclature )
            LEFT JOIN ref_nomenclatures.t_nomenclatures AS n19
                ON ( s.id_nomenclature_determination_method = n19.id_nomenclature )
            LEFT JOIN ref_nomenclatures.t_nomenclatures AS n20
                ON ( s.id_nomenclature_behaviour = n20.id_nomenclature )
            LEFT JOIN ref_nomenclatures.t_nomenclatures AS n21
                ON ( s.id_nomenclature_valid_status = n21.id_nomenclature )
            LEFT JOIN ref_nomenclatures.t_nomenclatures AS n22
                ON ( s.id_nomenclature_biogeo_status = n22.id_nomenclature )
            LEFT JOIN ref_habitats.habref AS hab
                ON ( hab.cd_hab = s.cd_hab ) ;
    """)

    op.execute("""
    ALTER TABLE ref_geo.bib_areas_types
        ADD COLUMN size_hierarchy INT default NULL;

    COMMENT ON COLUMN ref_geo.bib_areas_types.size_hierarchy IS
        'Diamètre moyen en mètres de ce type zone. Permet d''établir une hiérarchie des types '
        'de zone géographique. Utile pour le floutage des observations.' ;
    """)

    op.execute("""
    UPDATE ref_geo.bib_areas_types SET size_hierarchy = 200000 WHERE type_code = 'REG' ;
    UPDATE ref_geo.bib_areas_types SET size_hierarchy = 75000 WHERE type_code = 'DEP' ;
    UPDATE ref_geo.bib_areas_types SET size_hierarchy = 5000 WHERE type_code = 'COM' ;
    UPDATE ref_geo.bib_areas_types SET size_hierarchy = 10000 WHERE type_code = 'M10' ;
    UPDATE ref_geo.bib_areas_types SET size_hierarchy = 5000 WHERE type_code = 'M5' ;
    UPDATE ref_geo.bib_areas_types SET size_hierarchy = 1000 WHERE type_code = 'M1' ;
    """)


def downgrade():
    op.execute("""
    ALTER TABLE ref_geo.bib_areas_types
        DROP COLUMN size_hierarchy;
    """)

    op.execute("""
    DROP VIEW gn_synthese.v_synthese_for_export;
    CREATE VIEW gn_synthese.v_synthese_for_export
    AS SELECT s.date_min::date AS date_debut,
        s.date_max::date AS date_fin,
        s.date_min::time without time zone AS heure_debut,
        s.date_max::time without time zone AS heure_fin,
        t.cd_nom,
        t.cd_ref,
        t.nom_valide,
        t.nom_vern AS nom_vernaculaire,
        s.nom_cite,
        t.regne,
        t.group1_inpn,
        t.group2_inpn,
        t.classe,
        t.ordre,
        t.famille,
        t.id_rang AS rang_taxo,
        s.count_min AS nombre_min,
        s.count_max AS nombre_max,
        s.altitude_min AS alti_min,
        s.altitude_max AS alti_max,
        s.depth_min AS prof_min,
        s.depth_max AS prof_max,
        s.observers AS observateurs,
        s.id_digitiser,
        s.determiner AS determinateur,
        sa.communes,
        st_astext(s.the_geom_4326) AS geometrie_wkt_4326,
        st_x(s.the_geom_point) AS x_centroid_4326,
        st_y(s.the_geom_point) AS y_centroid_4326,
        st_asgeojson(s.the_geom_4326) AS geojson_4326,
        st_asgeojson(s.the_geom_local) AS geojson_local,
        s.place_name AS nom_lieu,
        s.comment_context AS comment_releve,
        s.comment_description AS comment_occurrence,
        s.validator AS validateur,
        n21.label_default AS niveau_validation,
        s.meta_validation_date AS date_validation,
        s.validation_comment AS comment_validation,
        s.digital_proof AS preuve_numerique_url,
        s.non_digital_proof AS preuve_non_numerique,
        d.dataset_name AS jdd_nom,
        d.unique_dataset_id AS jdd_uuid,
        d.id_dataset AS jdd_id,
        af.acquisition_framework_name AS ca_nom,
        af.unique_acquisition_framework_id AS ca_uuid,
        d.id_acquisition_framework AS ca_id,
        s.cd_hab AS cd_habref,
        hab.lb_code AS cd_habitat,
        hab.lb_hab_fr AS nom_habitat,
        s."precision" AS precision_geographique,
        n1.label_default AS nature_objet_geo,
        n2.label_default AS type_regroupement,
        s.grp_method AS methode_regroupement,
        n3.label_default AS technique_observation,
        n5.label_default AS biologique_statut,
        n6.label_default AS etat_biologique,
        n22.label_default AS biogeographique_statut,
        n7.label_default AS naturalite,
        n8.label_default AS preuve_existante,
        n9.label_default AS niveau_precision_diffusion,
        n10.label_default AS stade_vie,
        n11.label_default AS sexe,
        n12.label_default AS objet_denombrement,
        n13.label_default AS type_denombrement,
        n14.label_default AS niveau_sensibilite,
        n15.label_default AS statut_observation,
        n16.label_default AS floutage_dee,
        n17.label_default AS statut_source,
        n18.label_default AS type_info_geo,
        n19.label_default AS methode_determination,
        n20.label_default AS comportement,
        s.reference_biblio,
        s.id_synthese,
        s.entity_source_pk_value AS id_origine,
        s.unique_id_sinp AS uuid_perm_sinp,
        s.unique_id_sinp_grp AS uuid_perm_grp_sinp,
        s.meta_create_date AS date_creation,
        s.meta_update_date AS date_modification,
        COALESCE(s.meta_update_date, s.meta_create_date) AS derniere_action
       FROM gn_synthese.synthese s
         JOIN taxonomie.taxref t ON t.cd_nom = s.cd_nom
         JOIN gn_meta.t_datasets d ON d.id_dataset = s.id_dataset
         JOIN gn_meta.t_acquisition_frameworks af ON d.id_acquisition_framework = af.id_acquisition_framework
         LEFT JOIN ( SELECT cas.id_synthese,
                string_agg(DISTINCT a_1.area_name::text, ', '::text) AS communes
               FROM gn_synthese.cor_area_synthese cas
                 LEFT JOIN ref_geo.l_areas a_1 ON cas.id_area = a_1.id_area
                 JOIN ref_geo.bib_areas_types ta ON ta.id_type = a_1.id_type AND ta.type_code::text = 'COM'::text
              GROUP BY cas.id_synthese) sa ON sa.id_synthese = s.id_synthese
         LEFT JOIN ref_nomenclatures.t_nomenclatures n1 ON s.id_nomenclature_geo_object_nature = n1.id_nomenclature
         LEFT JOIN ref_nomenclatures.t_nomenclatures n2 ON s.id_nomenclature_grp_typ = n2.id_nomenclature
         LEFT JOIN ref_nomenclatures.t_nomenclatures n3 ON s.id_nomenclature_obs_technique = n3.id_nomenclature
         LEFT JOIN ref_nomenclatures.t_nomenclatures n5 ON s.id_nomenclature_bio_status = n5.id_nomenclature
         LEFT JOIN ref_nomenclatures.t_nomenclatures n6 ON s.id_nomenclature_bio_condition = n6.id_nomenclature
         LEFT JOIN ref_nomenclatures.t_nomenclatures n7 ON s.id_nomenclature_naturalness = n7.id_nomenclature
         LEFT JOIN ref_nomenclatures.t_nomenclatures n8 ON s.id_nomenclature_exist_proof = n8.id_nomenclature
         LEFT JOIN ref_nomenclatures.t_nomenclatures n9 ON s.id_nomenclature_diffusion_level = n9.id_nomenclature
         LEFT JOIN ref_nomenclatures.t_nomenclatures n10 ON s.id_nomenclature_life_stage = n10.id_nomenclature
         LEFT JOIN ref_nomenclatures.t_nomenclatures n11 ON s.id_nomenclature_sex = n11.id_nomenclature
         LEFT JOIN ref_nomenclatures.t_nomenclatures n12 ON s.id_nomenclature_obj_count = n12.id_nomenclature
         LEFT JOIN ref_nomenclatures.t_nomenclatures n13 ON s.id_nomenclature_type_count = n13.id_nomenclature
         LEFT JOIN ref_nomenclatures.t_nomenclatures n14 ON s.id_nomenclature_sensitivity = n14.id_nomenclature
         LEFT JOIN ref_nomenclatures.t_nomenclatures n15 ON s.id_nomenclature_observation_status = n15.id_nomenclature
         LEFT JOIN ref_nomenclatures.t_nomenclatures n16 ON s.id_nomenclature_blurring = n16.id_nomenclature
         LEFT JOIN ref_nomenclatures.t_nomenclatures n17 ON s.id_nomenclature_source_status = n17.id_nomenclature
         LEFT JOIN ref_nomenclatures.t_nomenclatures n18 ON s.id_nomenclature_info_geo_type = n18.id_nomenclature
         LEFT JOIN ref_nomenclatures.t_nomenclatures n19 ON s.id_nomenclature_determination_method = n19.id_nomenclature
         LEFT JOIN ref_nomenclatures.t_nomenclatures n20 ON s.id_nomenclature_behaviour = n20.id_nomenclature
         LEFT JOIN ref_nomenclatures.t_nomenclatures n21 ON s.id_nomenclature_valid_status = n21.id_nomenclature
         LEFT JOIN ref_nomenclatures.t_nomenclatures n22 ON s.id_nomenclature_biogeo_status = n22.id_nomenclature
         LEFT JOIN ref_habitats.habref hab ON hab.cd_hab = s.cd_hab;
    """)
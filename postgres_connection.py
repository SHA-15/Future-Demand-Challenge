import psycopg2
import time
from datetime import datetime
import pandas as pd

pd.set_option("display.max_colwidth", None)

x = [['Tue 13.08.', '19.30', 'KKL Luzern, Concert Hall', 'Elgar', 'Ljatoschynskyj', 'Respighi', '12 pm (CET) starting at CHF 50'], ['Wed 14.08.', '19.30', 'KKL Luzern, Concert Hall', 'Britten', 'Strauss', '12 pm (CET) starting at CHF 50'], ['Fri 16.08.', '18.30', 'KKL Luzern, Concert Hall', '12 pm (CET) starting at CHF 40'], ['Sat 17.08.', '18.30', 'KKL Luzern, Concert Hall', 'Grieg', 'Schumann', '12 pm (CET) starting at CHF 40'], ['Sun 18.08.', '11.00', 'KKL Luzern, Concert Hall', '12 pm (CET) starting at CHF 30'], ['Sun 18.08.', '15.30', 'KKL Luzern, Lucerne Hall', 'Rihm', 'Furrer', 'Streich', '12 pm (CET) starting at CHF 50'], ['Sun 18.08.', '19.30', 'KKL Luzern, Concert Hall', 'Schoenberg', '12 pm (CET) starting at CHF 30'], ['Mon 19.08.', '19.30', 'KKL Luzern, Concert Hall', 'de Séverac', 'Chopin', 'Prokofiev', 'Schumann', '12 pm (CET) starting at CHF 30'], ['Tue 20.08.', '19.30', 'KKL Luzern, Concert Hall', '12 pm (CET) starting at CHF 40'], ['Wed 21.08.', '17.00', 'KKL Luzern, Concert Hall', '12 pm (CET) starting at CHF 30'], ['Thu 22.08.', '12.15', 'Lukaskirche', '12 pm (CET) starting at CHF 30'], ['Thu 22.08.', '19.30', 'KKL Luzern, Concert Hall', 'Schubert', '12 pm (CET) starting at CHF 30'], ['Fri 23.08.', '19.30', 'KKL Luzern, Concert Hall', '12 pm (CET) starting at CHF 30'], ['Sat 24.08.', '11.00', 'KKL Luzern, Lucerne Hall', 'Streich', 'Rihm', 'Boulez', '12 pm (CET) starting at CHF 50'], ['Sat 24.08.', '18.30', 'KKL Luzern, Concert Hall', 'Bruckner', '12 pm (CET) starting at CHF 40'], ['Sat 24.08.', '21.30', 'Luzerner Theater, Theatersaal', 'Gnattali', 'Brouwer', 'Marino Arcaro', 'Piazzolla', '12 pm (CET) starting at CHF 50'], ['Sun 25.08.', '14.30', 'KKL Luzern, Lucerne Hall', '12 pm (CET) starting at CHF 50'], ['Sun 25.08.', '18.30', 'KKL Luzern, Concert Hall', 'Mozart', 'Debussy', 'Ravel', '12 pm (CET) starting at CHF 30'], ['Mon 26.08.', '19.30', 'KKL Luzern, Concert Hall', '12 pm (CET) starting at CHF 30'], ['Tue 27.08.', '12.15', 'Lukaskirche', '12 pm (CET) starting at CHF 30'], ['Tue 27.08.', '19.30', 'KKL Luzern, Concert Hall', '12 pm (CET) starting at CHF 30'], ['Wed 28.08.', '19.30', 'KKL Luzern, Concert Hall', '12 pm (CET) starting at CHF 40'], ['Thu 29.08.', '12.15', 'Lukaskirche', 'Strauss', 'Kirchner', 'Vignery', '12 pm (CET) starting at CHF 30'], ['Thu 29.08.', '19.30', 'KKL Luzern, Concert Hall', '12 pm (CET) starting at CHF 40'], ['Fri 30.08.', '19.30', 'KKL Luzern, Concert Hall', 'Beethoven', 'Fauré', 'Ravel', '12 pm (CET) starting at CHF 40'], ['Sat 31.08.', '11.00', 'KKL Luzern, Lucerne Hall', '12 pm (CET) starting at CHF 50'], ['Sat 31.08.', '16.00', 'Lukaskirche, Kirchensaal', '12 pm (CET) starting at CHF 50'], ['Sat 31.08.', '19.30', 'KKL Luzern, Concert Hall', 'Streich', 'Feldman', '12 pm (CET) starting at CHF 30'], ['Sun 01.09.', '11.00', 'KKL Luzern, Concert Hall', 'Widmann', 'Schumann', '12 pm (CET) starting at CHF 30'], ['Sun 01.09.', '16.00', 'Luzerner Theater, Theatersaal', '12 pm (CET) starting at CHF 50'], ['Sun 01.09.', '18.30', 'KKL Luzern, Concert Hall', 'Tchaikovsky', '12 pm (CET) starting at CHF 40'], ['Mon 02.09.', '19.30', 'Nr. 241323', 'KKL Luzern, Concert Hall', '12 pm (CET) starting at CHF 40'], ['Tue 03.09.', '12.15', 'Lukaskirche', 'Debussy', 'Holliger', 'Elgar', 'Schnyder', '12 pm (CET) starting at CHF 30'], ['Tue 03.09.', '19.30', 'KKL Luzern, Concert Hall', 'Marsalis', 'Price', '12 pm (CET) starting at CHF 30'], ['Wed 04.09.', '19.30', 'KKL Luzern, Concert Hall', 'Bruckner', '12 pm (CET) starting at CHF 40'], ['Thu 05.09.', '12.15', 'Lukaskirche', 'Schumann', 'Mendelssohn', 'Nielsen', 'Gubaidulina', '12 pm (CET) starting at CHF 30'], ['Thu 05.09.', '19.30', 'KKL Luzern, Concert Hall', 'Berlioz', '12 pm (CET) starting at CHF 40'], ['Fri 06.09.', '19.30', 'KKL Luzern, Concert Hall', 'Strauss', '12 pm (CET) starting at CHF 40'], ['Sat 07.09.', '11.00', 'Hochschule Luzern – Music, Salquin Concert Hall', 'Streich', '12 pm (CET) starting at CHF 50'], ['Sat 07.09.', '14.30', 'KKL Luzern, Concert Hall', 'Norman', 'Abrahamsen', '12 pm (CET) starting at CHF 30'], ['Sat 07.09.', '19.30', 'Nr. 241328', 'KKL Luzern, Concert Hall', '12 pm (CET) starting at CHF 40'], ['Sun 08.09.', '11.00', 'KKL Luzern, Concert Hall', '12 pm (CET) starting at CHF 30'], ['Sun 08.09.', '16.00', 'Hochschule Luzern – Music, Salquin Concert Hall', '12 pm (CET) starting at CHF 50'], ['Sun 08.09.', '19.30', 'KKL Luzern, Concert Hall', '12 pm (CET) starting at CHF 40'], ['Mon 09.09.', '19.30', 'KKL Luzern, Concert Hall', 'Dvořák', '12 pm (CET) starting at CHF 30'], ['Tue 10.09.', '12.15', 'Lukaskirche', '12 pm (CET) starting at CHF 30'], ['Tue 10.09.', '19.30', 'KKL Luzern, Concert Hall', 'Beethoven', 'Chopin', '12 pm (CET) starting at CHF 30'], ['Wed 11.09.', '19.30', 'KKL Luzern, Concert Hall', 'Mahler', '12 pm (CET) starting at CHF 30'], ['Thu 12.09.', '12.15', 'Lukaskirche', 'Liszt', 'Zhao', 'Gershwin', '12 pm (CET) starting at CHF 30'], ['Thu 12.09.', '19.30', 'KKL Luzern, Concert Hall', 'Dutilleux', 'Seltenreich', 'Ben-Haim', '12 pm (CET) starting at CHF 30'], ['Fri 13.09.', '19.30', 'KKL Luzern, Concert Hall', 'Bruckner', '12 pm (CET) starting at CHF 40'], ['Sat 14.09.', '18.30', 'KKL Luzern, Concert Hall', 'Bartók', 'Dvořák', '12 pm (CET) starting at CHF 30'], ['Sun 15.09.', '18.30', 'KKL Luzern, Concert Hall', '12 pm (CET) starting at CHF 30']]
image_link_array = ['https://www.lucernefestival.ch/media/thumbnails/filer_public/7e/8c/7e8cc114-18d2-4b2e-a504-686db42a430b/youth_symphony_orchestra_of_ukraine_lyniv2_c_mutesouvenir_kaibienert.jpg__300x200_q85_crop_subject_location-1470%2C847_subsampling-2_upscale.jpg', 'https://www.lucernefestival.ch/media/thumbnails/filer_public/df/4f/df4f34e3-6bd0-460b-bb06-05f7f7c4ffc4/euyo_2023_sven-kristian_wolf.jpg__300x200_q85_crop_subject_location-2912%2C1764_subsampling-2_upscale.jpg', 'https://www.lucernefestival.ch/media/thumbnails/filer_public/d3/25/d325af82-6571-429e-b27a-aac0df8ac7f2/220812_lfo_1_lfo_chailly_c_priskaketterer_lucerne_festival_14_approved.jpg__300x200_q85_crop_subject_location-2205%2C1533_subsampling-2_upscale.jpg', 'https://www.lucernefestival.ch/media/thumbnails/filer_public/5a/ee/5aee93c9-6c70-4ecf-ac02-63a2351f5269/klaus_makela_2_mathias_benuigui_pasco_and_co.jpg__300x200_q85_crop_subject_location-2247%2C2142_subsampling-2_upscale.jpg', 'https://www.lucernefestival.ch/media/thumbnails/filer_public/62/2d/622d9412-0528-4319-b831-1e924acf2c7c/230813_lfo_3_solist_innen_lfo_c_manuelajans_lucerne_festival_klein-36.jpg__300x200_q85_crop_subject_location-4095%2C2750_subsampling-2_upscale.jpg', 'https://www.lucernefestival.ch/media/thumbnails/filer_public/88/5e/885e4388-89ea-462d-8339-2b85fd190344/230827_lfa_5_lfco_c_peterfischli_lucerne_festival_2.jpg__300x200_q85_crop_subject_location-1680%2C1120_subsampling-2_upscale.jpg', 'https://www.lucernefestival.ch/media/thumbnails/filer_public/a5/6f/a56f5697-face-4b72-91fd-3a3520419241/404-190818_19309_sommer_sk_2_west_eastern_barenboim_mutter_c_fischli_02.jpg__300x200_q85_crop_subject_location-1104%2C784_subsampling-2_upscale.jpg', 'https://www.lucernefestival.ch/media/thumbnails/filer_public/61/9a/619ab420-c333-4cc8-a1b2-6fd2e89b0688/fujita_mao5_c_dovile_sermokas__sony_music_entertainmentjpg.jpg__300x200_q85_crop_subject_location-3016%2C1624_subsampling-2_upscale.jpg', 'https://www.lucernefestival.ch/media/thumbnails/filer_public/cb/31/cb31e8b1-3bf5-47d5-8700-7750ba76fb0e/malofeevalexander_c_liudmilamaloteeva.jpg__300x200_q85_crop_subject_location-495%2C441_subsampling-2_upscale.jpg', 'https://www.lucernefestival.ch/media/thumbnails/filer_public/92/55/9255a6e8-9273-479d-946a-55fb27c52e51/nagano-antoinesaito_approved.jpg__300x200_q85_crop_subject_location-2415%2C1622_subsampling-2_upscale.jpg', 'https://www.lucernefestival.ch/media/thumbnails/filer_public/34/41/3441c59d-91d8-4817-bda8-072bb04950f4/gafner_c_patrick_martin.jpg__300x200_q85_crop_subject_location-520%2C310_subsampling-2_upscale.jpg', 'https://www.lucernefestival.ch/media/thumbnails/filer_public/e2/4f/e24fd064-7c17-4258-8958-e724dd9aea08/sanderlingmichael010_c_philippschmidliluzernersinfonieorchester.jpg__300x200_q85_crop_subject_location-2940%2C1624_subsampling-2_upscale.jpg', 'https://www.lucernefestival.ch/media/thumbnails/filer_public/07/fb/07fb5b62-318d-48c6-bc6b-a58e54b79cf3/sheku_song_photo_5_credit_ollie_ali.jpg__300x200_q85_crop_subject_location-2163%2C2793_subsampling-2_upscale.jpg', 'https://www.lucernefestival.ch/media/thumbnails/filer_public/2a/b2/2ab285e5-7fed-4a4b-814d-7bd4f0ea0953/ruthr-101418meyerson_ricostudios-9180.jpg__300x200_q85_crop_subject_location-2520%2C1680_subsampling-2_upscale.jpg', 'https://www.lucernefestival.ch/media/thumbnails/filer_public/35/53/355375e0-47cc-46d3-9076-1d31b28b3a59/230819_lfo_5_nezet-seguin_c_patrickhurlimann_lucerne_festival_11.jpg__300x200_q85_crop_subject_location-2756%2C572_subsampling-2_upscale.jpg', 'https://www.lucernefestival.ch/media/thumbnails/filer_public/4b/96/4b96ba16-a0c4-4f06-8a89-afc3f8b9567c/sheku_song_photo_4_credit_ollie_ali.jpg__300x200_q85_crop_subject_location-2163%2C2814_subsampling-2_upscale.jpg', 'https://www.lucernefestival.ch/media/thumbnails/filer_public/f4/5f/f45f154f-c955-49ce-b053-6c7e41f4e98d/220824_masterclass_conducting_dufresne_yoon_rajna_terzakis_c_priskaketterer_lucerne_festival_01.jpg__300x200_q85_crop_subject_location-2226%2C1365_subsampling-2_upscale.jpg', 'https://www.lucernefestival.ch/media/thumbnails/filer_public/5d/2d/5d2dddf5-4f48-4885-937d-ecfaf0efbc7a/shani_lahav__rpho_3__guido_pijper.jpg__300x200_q85_crop_subject_location-936%2C594_subsampling-2_upscale.jpg', 'https://www.lucernefestival.ch/media/thumbnails/filer_public/a3/57/a3574400-99ee-45a8-af5f-698392943351/batiashvili_2017_12_-2240_fin2.jpg__300x200_q85_crop_subject_location-856%2C1032_subsampling-2_upscale.jpg', 'https://www.lucernefestival.ch/media/thumbnails/filer_public/cd/63/cd639fbe-026b-4e3e-9a28-a731571aa240/bartlett_martin_james7_c_paul_marc_mitchell.jpg__300x200_q85_crop_subject_location-4173%2C2925_subsampling-2_upscale.jpg', 'https://www.lucernefestival.ch/media/thumbnails/filer_public/f4/5f/f45f4ccf-6001-4f68-970a-2e63e3cd8463/die-12-cellisten-c_stephanrohl.jpg__300x200_q85_crop_subject_location-735%2C490_subsampling-2_upscale.jpg', 'https://www.lucernefestival.ch/media/thumbnails/filer_public/ca/67/ca67900f-9327-4962-956f-ac5179a372bf/petrenko_bphil_kp_monikarittershaus.jpg__300x200_q85_crop_subject_location-2415%2C1610_subsampling-2_upscale.jpg', 'https://www.lucernefestival.ch/media/thumbnails/filer_public/a1/95/a195bd0c-c0d3-4fd6-a6d1-f6b8145fc7a6/federleannemarie_c_fabiodepaola.jpeg__300x200_crop_subject_location-2185%2C1539_subsampling-2_upscale.jpeg', 'https://www.lucernefestival.ch/media/thumbnails/filer_public/df/02/df025c59-37de-4edf-a1a9-4b07bc9709f6/03-19_prom_66_cr_bbc_chris_christodoulou_1.jpg__300x200_q85_crop_subject_location-945%2C630_subsampling-2_upscale.jpg', 'https://www.lucernefestival.ch/media/thumbnails/filer_public/7e/11/7e11de7f-caf3-4c45-8329-58dd7259ae2a/lb_4441.jpg__300x200_q85_crop_subject_location-2142%2C1407_subsampling-2_upscale.jpg', 'https://www.lucernefestival.ch/media/thumbnails/filer_public/4e/de/4ede2879-a274-4edd-8679-d6bf2bb0670b/230822_proben_composer_seminar_iema_zinca_c_priskaketterer_lucerne_festival_24.jpg__300x200_q85_crop_subject_location-2205%2C1470_subsampling-2_upscale.jpg', 'https://www.lucernefestival.ch/media/thumbnails/filer_public/28/65/2865c1a9-818e-4c9a-986e-da2a1e4469a8/sheku_song_photo_3_credit_ollie_ali.jpg__300x200_q85_crop_subject_location-2205%2C3308_subsampling-2_upscale.jpg', 'https://www.lucernefestival.ch/media/thumbnails/filer_public/f1/6a/f16ad071-202a-4be5-b64e-84a9150e62fc/furrer_beat_9_c_manutheobald.jpg__300x200_q85_crop_subject_location-1456%2C1834_subsampling-2_upscale.jpg', 'https://www.lucernefestival.ch/media/thumbnails/filer_public/5c/10/5c1024f0-7cd9-4de9-b433-a9e15eaea289/anna_vinnitskaya_7337_full_c_bjoernkadenbach.jpg__300x200_q85_crop_subject_location-2940%2C1680_subsampling-2_upscale.jpg', 'https://www.lucernefestival.ch/media/thumbnails/filer_public/c6/68/c668c38f-55e4-4c4c-af08-ab210023ea37/klangforumwien_c_klangforumat.jpeg__300x200_crop_subject_location-945%2C846_subsampling-2_upscale.jpeg', 'https://www.lucernefestival.ch/media/thumbnails/filer_public/a7/e9/a7e9d4d7-3fa4-4463-841c-71250649d31c/vo_1_c_markus_jans.jpg__300x200_q85_crop_subject_location-424%2C360_subsampling-2_upscale.jpg', 'https://www.lucernefestival.ch/media/thumbnails/filer_public/11/ee/11ee0e9c-ea3a-427e-bc0e-42c8d33cb22c/rattle_220904_lso_2_rattle_c_manuelajans_lucerne_festival_16.jpg__300x200_q85_crop_subject_location-4095%2C2496_subsampling-2_upscale.jpg', 'https://www.lucernefestival.ch/media/thumbnails/filer_public/cb/fc/cbfc1de9-a5e8-4c9f-9310-864640d69eac/plath_theo_credit_marco_borggreve.jpg__300x200_q85_crop_subject_location-3885%2C2609_subsampling-2_upscale.jpg', 'https://www.lucernefestival.ch/media/thumbnails/filer_public/4b/93/4b935722-9aee-46d7-8fb7-19ee9acbfee1/hall-tompkins_kelly2_c_r_gregory_routt.jpg__300x200_q85_crop_subject_location-1248%2C1068_subsampling-2_upscale.jpg', 'https://www.lucernefestival.ch/media/thumbnails/filer_public/e9/ac/e9accabe-ff73-48d1-a6ed-d70cfe98502e/trifonov_2017_cdarioacosta-02.jpg__300x200_q85_crop_subject_location-2100%2C1420_subsampling-2_upscale.jpg', 'https://www.lucernefestival.ch/media/thumbnails/filer_public/4f/57/4f578656-903e-4d12-a7af-bd48a1b01dba/isata_kanneh-mason_2023_s03-048_credit_david_venni.jpg__300x200_q85_crop_subject_location-3498%2C2244_subsampling-2_upscale.jpg', 'https://www.lucernefestival.ch/media/thumbnails/filer_public/dd/e8/dde89dd7-053d-48b4-b830-1ed4e488f5ba/lisa_0077hq.jpg__300x200_q85_crop_subject_location-3192%2C2508_subsampling-2_upscale.jpg', 'https://www.lucernefestival.ch/media/thumbnails/filer_public/41/68/4168c644-fd9f-4778-a97b-402741a46710/thielemann_christian_c_wienerphilharmoniker_dieternagl_dn012996.jpg__300x200_q85_crop_subject_location-1584%2C3024_subsampling-2_upscale.jpg', 'https://www.lucernefestival.ch/media/thumbnails/filer_public/fd/1c/fd1c6e78-6d5c-406a-af0c-f52273b8bb3c/230909_portrait_poppe_ensemble_helix_grimaitre_hunt_c_peterfischli_lucerne_festival_08.jpg__300x200_q85_crop_subject_location-1680%2C1120_subsampling-2_upscale.jpg', 'https://www.lucernefestival.ch/media/thumbnails/filer_public/96/15/96156340-0aab-4acc-9748-10ccfaef2682/3_gb_with_mco_credit_christopher_christodoulou.jpg__300x200_q85_crop_subject_location-1890%2C1152_subsampling-2_upscale.jpg', 'https://www.lucernefestival.ch/media/thumbnails/filer_public/92/c1/92c1605e-e655-4d1b-8de2-dad770837086/hagen_julia_web_small-33julia_hagen__c__simon_pauly.jpg__300x200_q85_crop_subject_location-1470%2C854_subsampling-2_upscale.jpg', 'https://www.lucernefestival.ch/media/thumbnails/filer_public/8f/d6/8fd64a98-4755-42ff-94f2-c1d98052a591/lea-desandre-c-monika-rittershaus-4-2000x1313.jpg__300x200_q85_crop_subject_location-945%2C621_subsampling-2_upscale.jpg', 'https://www.lucernefestival.ch/media/thumbnails/filer_public/59/26/5926525b-5bc6-4f6d-b634-cc01404c69fb/220824_masterclass_conducting_lfco_c_priskaketterer_lucerne_festival_01.jpg__300x200_q85_crop_subject_location-1953%2C1071_subsampling-2_upscale.jpg', 'https://www.lucernefestival.ch/media/thumbnails/filer_public/b9/71/b9718ede-81ca-43d5-9023-d74d93143a3c/nyp20220106bychrislee.jpg__300x200_q85_crop_subject_location-1472%2C752_subsampling-2_upscale.jpg', 'https://www.lucernefestival.ch/media/thumbnails/filer_public/8e/16/8e166455-058a-43d5-9f57-65354e14fb36/anna_prohaska011__marco_borggreve.jpg__300x200_q85_crop_subject_location-2625%2C2900_subsampling-2_upscale.jpg', 'https://www.lucernefestival.ch/media/thumbnails/filer_public/45/a8/45a8220b-b025-45e2-8b49-fc73e14625fe/adelphi_quartet_credit_roland_unger_7.jpg__300x200_q85_crop_subject_location-2100%2C1910_subsampling-2_upscale.jpg', 'https://www.lucernefestival.ch/media/thumbnails/filer_public/0b/65/0b65109f-a9d8-4443-bfb1-45f56297f029/buchbinderrudolf10_c_marcoborggrevejpg.jpg__300x200_q85_crop_subject_location-3016%2C1682_subsampling-2_upscale.jpg', 'https://www.lucernefestival.ch/media/thumbnails/filer_public/41/81/41815e50-3fe8-4183-8a7f-8c48f09f3d95/jaervi_paavo_c_albertovenzago.jpg__300x200_q85_crop_subject_location-2808%2C2808_subsampling-2_upscale.jpg', 'https://www.lucernefestival.ch/media/thumbnails/filer_public/ed/a9/eda9599a-09c5-4871-90c0-4d21ef45a9fe/zhaomelodie_c_karlanewton_011.jpg__300x200_q85_crop_subject_location-2884%2C1932_subsampling-2_upscale.jpg', 'https://www.lucernefestival.ch/media/thumbnails/filer_public/4f/9f/4f9f3c6d-837b-4942-b138-3f127f95bbad/renaud_capucon_1_cred_warner.jpg__300x200_q85_crop_subject_location-3848%2C1850_subsampling-2_upscale.jpg', 'https://www.lucernefestival.ch/media/thumbnails/filer_public/89/5f/895f7e3f-b110-4576-9f5f-b4f0e5ae39c4/shani_lahav_070_credit_marco_borggreve.jpg__300x200_q85_crop_subject_location-3531%2C1914_subsampling-2_upscale.jpg', 'https://www.lucernefestival.ch/media/thumbnails/filer_public/ad/1b/ad1b983d-0735-4ef9-b720-1e1f8bb28e9d/kopatchinskaja-patricia_copyrightmarcoborggreve003.jpeg__300x200_crop_subject_location-1236%2C696_subsampling-2_upscale.jpeg', 'https://www.lucernefestival.ch/media/thumbnails/filer_public/55/0c/550c5b95-af69-472f-9640-3c493c7dd062/gilbert_alan_c_marcoborggreve_ndr.jpg__300x200_q85_crop_subject_location-3675%2C2450_subsampling-2_upscale.jpg']
title_list = ['Youth Symphony Orchestra of Ukraine | Oksana Lyniv', 'European Union Youth Orchestra | Gianandrea Noseda | Nicolas Altstaedt', 'Lucerne Festival Orchestra | Riccardo Chailly', 'Lucerne Festival Orchestra | Klaus Mäkelä | Leif Ove Andsnes', 'Soloists of the Lucerne Festival Orchestra', 'Soloists of the Lucerne Festival Contemporary Orchestra (LFCO)', 'West-Eastern Divan Orchestra | Daniel Barenboim | Anne-Sophie Mutter', 'Mao Fujita', 'Lucerne Festival Orchestra | Riccardo Chailly | Alexander Malofeev', 'Dresden Festival Orchestra | Concerto Köln | Kent Nagano', 'Tjasha Gafner', 'Lucerne Symphony Orchestra | Michael Sanderling | Francesco Piemontesi', 'Czech Philharmonic | Jakub Hrůša | Sheku Kanneh-Mason', 'Lucerne Festival Contemporary Orchestra (LFCO) | Ruth Reinhardt', 'Lucerne Festival Orchestra | Yannick Nézet-Séguin | Beatrice Rana', 'Sheku Kanneh-Mason | Plínio Fernandes', 'Lucerne Festival Contemporary Orchestra (LFCO) | Participants in the Contemporary-Conducting Program', 'Rotterdam Philharmonic Orchestra | Lahav Shani | Lisa Batiashvili', 'Lisa Batiashvili | Giorgi Gigashvili | Tsotne Zedginidze', 'Martin James Bartlett', 'The 12 Cellists of the Berliner Philharmoniker', 'Kirill Petrenko | Berliner Philharmoniker', 'Annemarie Federle', 'Berliner Philharmoniker | Kirill Petrenko', 'Royal Concertgebouw Orchestra | Myung-Whun Chung | Sir András Schiff', 'International Ensemble Modern Academy (IEMA Ensemble 2023-24) | Participants in the Contemporary-Conducting Program', 'Harry Baker | Sheku Kanneh-Mason', 'Lucerne Festival Contemporary Orchestra (LFCO) | Beat Furrer | Simon Höfele', 'Anna Vinnitskaya', 'Klangforum Wien | Cantando Admont | Beat Furrer', 'The Cleveland Orchestra | Franz Welser-Möst | Víkingur Ólafsson', 'Bavarian Radio Symphony Orchestra | Sir Simon Rattle', 'Theo Plath | Aris Alexander Blettenberg', 'Chineke! Orchestra | Leslie Suganandarajah | Kelly Hall-Tompkins', 'Leipzig Gewandhaus Orchestra | Andris Nelsons | Daniil Trifonov', 'Isata Kanneh-Mason', 'Orchestre de Paris | Klaus Mäkelä | Lisa Batiashvili', 'Vienna Philharmonic | Christian Thielemann', 'Ensemble Helix, Studio for Contemporary Music at the Hochschule Luzern – Musik | Beat Furrer', 'Lucerne Festival Contemporary Orchestra (LFCO) | Sir George Benjamin | Jörgen van Rijen', 'Vienna Philharmonic | Christian Thielemann | Julia Hagen', 'Jupiter Ensemble | Thomas Dunford | Lea Desandre', 'Ensemble of the Lucerne Festival Contemporary Orchestra (LFCO) | Participants in the Contemporary-Conducting Program', 'Staatskapelle Berlin | Susanna Mälkki | Eric Cutler | Wiebke Lehmkuhl', 'Mahler Chamber Orchestra | Antonello Manacorda | Anna Prohaska', 'Adelphi Quartet', 'Rudolf Buchbinder', 'Zurich Tonhalle Orchestra | Paavo Järvi | Sheku Kanneh-Mason', 'Mélodie Zhao', 'Munich Philharmonic | Lahav Shani | Renaud Capuçon', 'Munich Philharmonic | Lahav Shani', 'Budapest Festival Orchestra', 'NDR Elbphilharmonie Orchester | NDR Vokalensemble | MDR-Rundfunkchor | Alan Gilbert']

#-------X PROVIDES DATE, TIME, LOCATION------------
current_year = datetime.now().year

date_list = []
for sub_list in range(len(x)):
    date_string = x[sub_list][0]
    date = datetime.strptime(date_string, "%a %d.%m.")
    date = date.replace(year=current_year)
    date = date.strftime("%d-%m-%Y")
    date_list.append(date)

time_list = []
for sub_time in range(len(x)):
    time_string = x[sub_time][1]
    time_format = datetime.strptime(time_string, "%H.%M")
    time_format = time_format.strftime("%H:%M")
    time_list.append(time_format)

locations_list = []
for loc_index in range(len(x)):
    event_location = x[loc_index][2]
    if "Nr. 24" in event_location:
        event_location = x[loc_index][3]
        locations_list.append(event_location)
    else:
        locations_list.append(event_location)
#-----------------------CREATE DATAFRAME OBJECTS FOR EVENT, LOCATION, PERFORMERS------------------
location_df = pd.DataFrame(
    {
        "event_location": locations_list
    }
)

event_date = []
event_time = []
event_title = []
event_image = []
event_performer = []
event_location = []

for index, title in enumerate(title_list):
    performers = title.split("|")
    # print(performers)
    performers = [performer.strip() for performer in performers]
    # print(performers)

    #Get_date for each other list:
    date = date_list[index]
    time_instance = time_list[index]
    location = locations_list[index]
    image_url = image_link_array[index]


    # print(f"Title Matching Index Count: {index}")
    #Time to append
    for performer in performers:
        event_date.append(date)
        event_time.append(time_instance)
        event_location.append(location)
        event_image.append(image_url)
        event_performer.append(performer)
        event_title.append(title)

#Establish Event Dataframe
event_df = pd.DataFrame(
    {
        "event_date": event_date,
        "event_time": event_time,
        "event_title": event_title,
        "event_location": event_location,
        "event_performer": event_performer,
        "event_image": event_image
    }
)

names_works_df = pd.read_csv(r"C:\Users\Izrum\Desktop\nandw.csv")
#-----------------------------READY DATAFRAME OBJECTS FOR POSTGRES PARSING----------------
location_df = location_df.drop_duplicates(subset="event_location", keep="first")
location_df.insert(0, "location_id", range(1, 1+len(location_df)))
location_df.reset_index(drop=True, inplace=True)

event_df.insert(0, "event_id", range(10000, 10000+len(event_df)))


names_works_df = names_works_df.drop_duplicates(subset = "name", keep="first")
names_works_df = names_works_df.rename(columns={"Unnamed: 0" : "performer_id"})
names_works_df = names_works_df.rename(columns={"name" : "event_performer"})
names_works_df["performer_id"] = range(100, 100 + len(names_works_df))
names_works_df.reset_index(drop=True, inplace=True)
#--------------------------------Build Connection To POSTGRES-----------------------------
def establish_connection(database_value="FutureDemand", user_value="postgres", password="abcd1234", host="localhost"):
    try:
        connection = psycopg2.connect(
            database=database_value,
            user=user_value,
            password=password,
            host=host
        )
        print("Database connection successful")

    except Exception as e:
        print(f"Table Creation Error: {e}")

    return connection

def tables_creation():
    # Creating Tables
    tables = (
        """
        CREATE TABLE location (
            id SERIAL PRIMARY KEY,
            location_name VARCHAR(50) NOT NULL
        )
        """,
        """
        CREATE TABLE performer (
            name VARCHAR(256) NOT NULL PRIMARY KEY,
            works TEXT
        )
        """,
        """
        CREATE TABLE event (
            id SERIAL PRIMARY KEY,
            event_name VARCHAR(256) NOT NULL,
            event_date TEXT NOT NULL,
            event_time TEXT NOT NULL,
            event_location VARCHAR(256) NOT NULL,
            performer_name VARCHAR(256) REFERENCES performer (name),
            event_image TEXT NOT NULL            
        )
        """
    )

    try:
        for table in tables:
            cursor.execute(
                """
                SELECT EXISTS (
                    SELECT 1
                    FROM information_schema.tables
                    WHERE table_name = %s
                )
                """, (table.split()[2],)
            )
            table_exists = cursor.fetchone()[0]
            if table_exists:
                print("Table already exists")
            else:
                cursor.execute(table)
                print("Table Creation Complete")
            #Allow Delay between Creations
            time.sleep(2)

        print("Tables created successfully")

    except Exception as e:
        print(f"Unable to create Tables: {e}")

    conn.commit()
#---------------------------MOVING DATA TO TABLES----------------------------------------
#MOVING LOCATION DATAFRAME TO LOCATION TABLE in POSTGRES
def location_data():
    for index in range(0, len(location_df)):
        values = (int(location_df["location_id"][index]), location_df["event_location"][index])
        print(f"starting index with value: {index}")
        cursor.execute("INSERT INTO location (id, location_name) VALUES (%s, %s)", values)
        print(f"success, Let's Keep on Going!")
        time.sleep(2)

    print("Location Records updated!")
    conn.commit()

#MOVING NAME WORKS DATAFRAME TO PERFORMER TABLE IN POSTGRES
def works_data():
    for index in range(0, len(names_works_df)):
        values = (int(names_works_df["performer_id"][index]), names_works_df["event_performer"][index], names_works_df["works"][index])
        print(f"starting index with value: {index}")
        cursor.execute("INSERT INTO performer (id, name, works) VALUES (%s, %s, %s)", values)
        print(f"success, Let's Keep on Going!")
        time.sleep(2)

    conn.commit()
    print("Performer Records updated!")

#Moving Events DATAFRAME to EVENT TABLE IN POSTGRES
def event_data():
    for index in range(0, len(event_df)):
        values = (
            int(event_df["event_id"][index]),
            event_df["event_date"][index],
            event_df["event_time"][index],
            event_df["event_title"][index],
            event_df["event_location"][index],
            event_df["event_performer"][index],
            event_df["event_image"][index]
        )
        print(f"starting index with value: {index}")
        cursor.execute("""INSERT INTO event (id, event_name, event_date, event_time, location, performer, event_image) 
                       VALUES (%s, %s, %s, %s, %s, %s, %s)""", values)
        print(f"success, Let's Keep on Going!")
        time.sleep(2)

    conn.commit()
    print("event records updated")


#--------------------------------COMMAND EXECUTION FOR POSTGRES-----------------------------------
# conn = establish_connection()
# cursor = conn.cursor()
#
# tables_creation()
#
# # time.sleep(2)
#
# location_data()
# #
# # time.sleep(2)
# #
# works_data()
# #
# # time.sleep(2)
#
# event_data()

event_df = event_df.merge(location_df, on="event_location", how="left")
event_df.drop("event_location", axis=1)

# event_df = event_df.merge(names_works_df["performer_id"], on="event_performer", how="left")
print(event_df.dtypes)
print(names_works_df.dtypes)
event_df.to_csv(r"C:\Users\Izrum\Desktop\events.csv")






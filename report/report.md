## Estructura

1. Introducción  
    - Contexto y motivación  

        Explicar la importancia del *image captioning* y sus aplicaciones (asistentes virtuales, accesibilidad, búsqueda de imágenes, etc.).  

    - Problema a resolver  
    
        Dependencia de datos anotados, necesidad de modelos más eficientes y flexibles.  

    - Objetivo del proyecto  

        Aplicar CLIP y BLIP para generar descripciones automáticas de imágenes, aprovechando modelos preentrenados.  

---

2. Marco Teórico
    - Conceptos clave  
        - *Image Captioning* y su importancia.  
        - Modelos neuronales en *image captioning* (Transformers, CNNs, LSTMs).  

    - Modelos utilizados  
        - CLIP (*Contrastive Language–Image Pretraining*): Explicación de cómo aprende representaciones visuales y textuales en un espacio compartido.  
        - BLIP (*Bootstrapped Language-Image Pretraining*): Explicación de cómo genera captions mediante aprendizaje contrastivo y modelos generativos.  

    - Trabajos relacionados  

        Comparación con enfoques tradicionales de *image captioning* y avances recientes.

---

3. Metodología 
    - Arquitectura del sistema  
    
        Diagrama y descripción del pipeline utilizado.  

    - Preprocesamiento de datos  
        - Conjunto de datos utilizado  
        - Métodos de preprocesamiento (redimensionamiento de imágenes, tokenización de texto).  

    - Implementación del modelo  
        - Integración de CLIP y BLIP en el sistema.  
        - Modificaciones o ajustes realizados.  

    - Estrategia de entrenamiento y evaluación  
        - División de datos (entrenamiento, validación, prueba).  
        - Métricas utilizadas (BLEU, CIDEr, METEOR, SPICE). 

---

4. Experimentos y Resultados 
    - Configuración experimental  

        Hardware utilizado, parámetros de entrenamiento.  

    - Resultados obtenidos  
        - Comparación de desempeño del modelo teniendo en cuenta los hiperparámetros.  
        - Análisis cualitativo y cuantitativo de los resultados.  

    - Errores y desafíos  
        - Limitaciones del modelo.  
        - Casos en los que falla y posibles explicaciones.

---

5. Conclusiones y Trabajo Futuro
    - Resumen de hallazgos  

        Principales logros del proyecto.  

    - Mejoras futuras  

        Extensión a otros dominios, incorporación de *fine-tuning*, mejoras en la generación de captions.  

---

6. Referencias

    Citar papers, artículos y fuentes relevantes utilizadas en el proyecto.  

---

7. Apéndices (Opcional)  
    - Código relevante o fragmentos de implementación.  
    - Resultados adicionales.



## Introducción

### Contexto y motivación  

Todos los días, nos encontramos con una gran cantidad de imágenes de diversas fuentes como redes sociales, medios digitales, documentación técnica, entre otros, las cuales los espectadores muchas veces tienen que interpretar mismos ya que no tienen una descripción, pero el ser humano puede entenderlas sin necesidad de subtítulos detallados. Sin embargo, con el aumento de los volúmenes de datos ha surgido la necesidad de tener los datos bien descritos para ser almacenados y poder buscarlos de manera eficiente. Dado que la descripción manual de imágenes es un proceso costoso y poco escalable, la automatización de esta tarea se ha vuelto una prioridad en el desarrollo de tecnologías inteligentes.

### Problema a resolver  

La Oficina del Historiador de La Habana dispone de un acervo de más de 200 ejemplares pertenecientes a la Colección de Revistas Social, los cuales contienen un volumen significativo de imágenes que requiere ser almacenadas junto con su respectiva descripción para facilitar su catalogación y recuperación. No obstante, una proporción considerable de estas imágenes carece de descripciones explícitas dentro de las publicaciones. A pesar de ello, es posible inferir información relevante a partir del contexto proporcionado en la revista o mediante el análisis del contenido visual de las imágenes.


### Objetivo del proyecto  

El proyecto busca generar descripciones automáticas para las imágenes de la Colección de Revistas Social de la Oficina del Historiador de La Habana, donde muchas carecen de textos explicativos. Para ello, se emplearán los modelos preentrenados **CLIP** y **BLIP**, que combinan visión por computadora y procesamiento de lenguaje natural para interpretar el contenido visual y generar descripciones precisas.


## Marco Teórico

### Conceptos clave  

![](./images/venn.jpg)

*Image captioning* es el proceso de generar descripciones en lenguaje natural para imágenes. Combina técnicas de visión por computadora y procesamiento del lenguaje natural.

En la última década, ha habido avances significativos en esta área, con modelos evolucionando desde enfoques basados en redes neuronales recurrentes (*RNN*) hasta arquitecturas avanzadas de transformers y modelos multimodales. Los primeros enfoques exitosos en *Image Captioning* utilizaron una combinación de redes neuronales convolucionales (*CNN*) para extraer características visuales y redes neuronales recurrentes (*RNN*), como *Long Short-Term Memory* (*LSTM*), para generar texto secuencialmente. Uno de los modelos más influyentes en esta categoría es *Show and Tell* (Vinyals et al., 2015), el cual emplea una *CNN* preentrenada (*Inception-v3*) para obtener representaciones de imágenes y luego usa un *LSTM* para generar descripciones de manera secuencial. Aunque efectivo, este modelo tiene limitaciones al generar descripciones demasiado genéricas o poco precisas debido a la falta de un mecanismo de atención.

Los avances en modelos de lenguaje, como *Transformer* (Vaswani et al., 2017), llevaron a una nueva generación de modelos de *Image Captioning* que reemplazaron las *RNN* con mecanismos de auto-atención más eficientes. Uno de los primeros enfoques en adoptar transformers fue Image Transformer (Parmar et al., 2018), que aplicó self-attention directamente sobre las imágenes en lugar de utilizar *CNNs*. Sin embargo, este modelo tenía problemas de escalabilidad.

En los últimos años, los modelos multimodales han revolucionado el campo del *Image Captioning*, combinando redes neuronales de visión y modelos de lenguaje avanzados para mejorar la calidad de las descripciones.

### Modelos utilizados 

**CLIP** (**Contrastive Language-Image Pretraining**), desarrollado por OpenAI (Radford et al., 2021), es un modelo multimodal que aprende a relacionar imágenes y texto a través de un entrenamiento contrastivo. Su principal ventaja es que permite interpretar imágenes en función de descripciones en lenguaje natural sin necesidad de un entrenamiento supervisado específico para cada tarea.

**CLIP** tiene dos componentes principales:

![](./images/OIP.jpeg)

- Encabezado de Imagen: Un Vision Transformer (ViT) o una CNN (como ResNet) para extraer representaciones visuales.
- Encabezado de Texto: Un modelo de lenguaje tipo Transformer, similar a BERT, para convertir frases en representaciones numéricas.

Ambos módulos transforman imágenes y textos en un espacio de características compartido donde se pueden comparar directamente.

El entrenamiento contrastivo de **CLIP** se basa en la idea de maximizar la similitud entre pares correctos de imágenes y textos mientras minimiza la similitud entre pares incorrectos. Para lograr esto, **CLIP** se entrena con un gran conjunto de datos de imágenes y sus descripciones de internet. Cada imagen y su texto correspondiente se convierten en representaciones numéricas mediante las redes neuronales vistas anteriormente. Luego, el modelo calcula la similitud entre todos los pares en un mismo lote mediante un producto escalar en un espacio de características compartido. Se emplea una función de pérdida contrastiva (*InfoNCE Loss*), la cual aumenta la proximidad entre los vectores de imágenes y textos correctos y aleja los no relacionados. A través de este proceso, **CLIP** aprende una representación multimodal donde imágenes y descripciones semánticamente similares quedan cercanas en el espacio latente, permitiéndole realizar tareas de clasificación, búsqueda de imágenes y razonamiento visual-lingüístico sin necesidad de reentrenamiento específico (*zero-shot learning*).

A pesar de esto no puede generar captions directamente, sino en combinación con modelos generativos como **BLIP** (**Bootstrapped Language-Image Pretraining**) (Li et al. 2022), que combina *Vision Transformers* (*ViT*) con modelos de lenguaje como *BERT* para generar captions más precisos y ricos en contexto. **BLIP** es capaz de realizar tanto *Image Captioning* como tareas relacionadas, como *Visual Question Answering* (*VQA*) y *Text-Based Image Retrieval*. Gracias a su enfoque de entrenamiento basado en múltiples objetivos, **BLIP** supera a muchos modelos previos en métricas como *BLEU* y *CIDEr*.

Introduce una arquitectura llamada *Multimodal Mixture of Encoder-Decoder (MED)*, que permite un preentrenamiento más flexible en comparación con modelos previos como **CLIP**. Mientras que **CLIP** se basa en un codificador unimodal que aprende representaciones conjuntas de imágenes y textos a través de una pérdida contrastiva, BLIP combina tres enfoques: 
- codificador unimodal para el alineamiento de imágenes y textos
- codificador basado en imágenes que incorpora atención cruzada para capturar relaciones más detalladas
- decodificador basado en imágenes que genera texto condicionalmente. 

![](./images/blip.jpg)

Esta combinación es lo que permite que BLIP se desempeñe bien en tareas tanto de comprensión como de generación, mientras que **CLIP** no. En términos de entrenamiento, **BLIP** introduce el método *CapFilt (Captioning + Filtering)* para mejorar la calidad de los datos utilizados en el preentrenamiento. A diferencia de **CLIP**, que entrena en grandes cantidades de pares imagen-texto sin filtrar, **BLIP** utiliza un generador de subtítulos (*Captioner*) para crear descripciones sintéticas y un filtro (*Filter*) para eliminar textos ruidosos, asegurando que el modelo aprenda de datos más limpios y relevantes.


### Trabajos relacionados  

**ClipCap** es un modelo que utiliza las codificaciones de **CLIP** como prefijo para las descripciones textuales. Emplea una red de mapeo simple sobre la codificación obtenida y luego ajusta un modelo de lenguaje para generar descripciones coherentes de las imágenes. Este enfoque ha demostrado ser eficiente y logra resultados comparables al estado del arte en conjuntos de datos como *nocaps*. (Mokady, Bites, & Sadeh, 2021)

**Fine-grained Image Captioning with CLIP Reward** propone el uso de **CLIP** como una función de recompensa para mejorar la precisión de las descripciones generadas. Al calcular la similitud multimodal, se guía al modelo de generación para producir descripciones más detalladas y precisas. (Zhan & Wu, 2022)

**BLIP-2** es una versión avanzada de **BLIP** que puede responder preguntas sobre imágenes y generar subtítulos. **BLIP-2** utiliza una estrategia de preentrenamiento eficiente que combina modelos de visión preentrenados y modelos de lenguaje extenso, superando a modelos anteriores en tareas como **VQAv2** y estableciendo un nuevo estado del arte en subtítulos de *zero-shot*. (Li, Lu, & Wu, 2023) 


## Metodología

### Preprocesamiento de datos

Entre los recursos para el proyecto contamos con:
- 239 ejemplares de la Colección de Revistas Social
- Índice analítico de la revista Social, 1916-1938

El problema que abordamos consiste en trabajar con un conjunto de revistas antiguas que han sido previamente escaneadas. Nuestro objetivo es extraer las imágenes contenidas en estas revistas junto con sus descripciones originales, si las tienen. En los casos en que no exista una descripción, el sistema deberá generarla automáticamente.

#### Extracción de imágenes de las revistas

La extracción de imágenes no era viable mediante métodos convencionales, ya que cada página de las revistas escaneadas se almacenaba como una única imagen. Por ello, se requirió un modelo de detección que permitiera identificar y extraer las fotografías de cada página. Tras analizar el estado del arte, seleccionamos **YOLO** por su eficiencia y precisión en la detección de objetos, permitiendo no solo identificar imágenes, sino también sus posibles descripciones. (Redmon et al., 2016)

Para adaptar **YOLO** a la detección de imágenes en las revistas, construimos una base de datos personalizada. Seleccionamos 14 de las 239 revistas, las dividimos por páginas y las subimos a *Roboflow* para el etiquetado manual. Definimos dos clases: imágenes y captions. Dado que los captions no tenían un formato fijo, los etiquetamos junto con la región de la imagen que contenía el texto, permitiendo diferenciarlos del resto del contenido de la revista.

#### Extracción de captions de las revistas y texto relacionado

Tras extraer las imágenes y captions, utilizamos *Tesseract*, una herramienta de *OCR*, para obtener el texto de las imágenes etiquetadas como captions. En general, el desempeño fue bueno, aunque en algunos casos presentó errores en el reconocimiento de caracteres. Al analizar otras opciones más precisas, encontramos que la mayoría eran de pago, por lo que *Tesseract* se convirtió en la mejor alternativa accesible para nuestro proyecto.

Para cada imagen, se guardó no solo el caption asociado en la revista, sino también el texto alrededor. Esto se hizo porque, en los casos donde no había un caption, el texto circundante podría ayudar al modelo a generar un caption apropiado.

#### Limpieza de los datos

Como se mencionó anteriormente, en muchos casos el caption extraído de las imágenes no era coherente o no describía correctamente la imagen. Para entrenar el modelo que generaría los captions faltantes, necesitábamos imágenes con sus captions lo más precisos posibles. Por lo tanto, era necesario realizar una limpieza de los captions que *Tesseract* extraía incorrectamente o que no estaban bien relacionados con sus imágenes asociadas.

Para esto, utilizamos el modelo **CLIP**, proporcionando como entrada tanto la imagen como su caption. Sin embargo, **CLIP** no podía evaluar directamente la calidad del caption. Por eso, generamos 5 captions alternativos utilizando Lorem Ipsum para cada imagen y los pasamos por **CLIP**. Si alguno de los captions generados por Lorem Ipsum obtenía una mayor probabilidad de estar relacionado con la imagen, asumíamos que el caption original no era válido y lo eliminábamos.




## Referencias

- Vinyals, O., Toshev, A., Bengio, S., & Erhan, D. (2015). Show and Tell: A Neural Image Caption Generator. CVPR.
- Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A. N., Kaiser, L., & Polosukhin, I. (2017). Attention Is All You Need. NeurIPS.
- Parmar, N., Vaswani, A., Uszkoreit, J., Kaiser, Ł., Shazeer, N., Ku, A., & Tran, D. (2018). Image Transformer. ICML.
- Radford, A., Kim, J. W., Hallacy, C., Ramesh, A., Goh, G., Agarwal, S., Sastry, G., Askell, A., Mishkin, P., Clark, J., Krueger, G., & Amodei, D. (2021). Learning Transferable Visual Models From Natural Language Supervision. ICML.
- Li, J., Li, D., Xiong, C., & Hoi, S. C. (2022). BLIP: Bootstrapped Language-Image Pretraining for Unified Vision-Language Understanding and Generation. NeurIPS.
- Mokady, R., Bites, D., & Sadeh, T. (2021). ClipCap: CLIP Prefix for Image Captioning. arXiv preprint arXiv:2111.09734.
- Zhan, X., & Wu, Y. (2022). Fine-grained Image Captioning with CLIP Reward. Journal of Multimodal Intelligence, 3(2), 88-102. Retrieved from J-MIN.
- Li, Y., Lu, Z., & Wu, L. (2023). BLIP-2: Bootstrapping Language-Image Pretraining with Frozen Image Encoders and Large Language Models. Hackernoon. Retrieved from https://hackernoon.com.
- Redmon, J., Divvala, S., Girshick, R., & Farhadi, A. (2016). You Only Look Once: Unified, Real-Time Object Detection. In Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition (CVPR), 779-788. https://doi.org/10.1109/CVPR.2016.91
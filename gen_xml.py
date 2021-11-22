import os
from xml.dom.minidom import Document 


def generate_xml(image_name,boxes,keypoints, img_size,xml_path):
    doc = Document()
    annotation = doc.createElement('annotation')
    doc.appendChild(annotation)

    title = doc.createElement('folder')
    title_text = doc.createTextNode('data')
    title.appendChild(title_text)
    annotation.appendChild(title)

    title = doc.createElement('filename')
    title_text = doc.createTextNode(image_name)
    title.appendChild(title_text)
    annotation.appendChild(title)

    source = doc.createElement('source')
    annotation.appendChild(source)

    title = doc.createElement('database')
    title_text = doc.createTextNode('TI Parking Spot data base')
    title.appendChild(title_text)
    source.appendChild(title)

    title = doc.createElement('annotation')
    title_text = doc.createTextNode('PASCAL VOC2007 Format')
    title.appendChild(title_text)
    source.appendChild(title)

    size = doc.createElement('size')
    annotation.appendChild(size)

    title = doc.createElement('width')
    title_text = doc.createTextNode(str(img_size[1]))
    title.appendChild(title_text)
    size.appendChild(title)

    title = doc.createElement('height')
    title_text = doc.createTextNode(str(img_size[0]))
    title.appendChild(title_text)
    size.appendChild(title)

    title = doc.createElement('depth')
    title_text = doc.createTextNode(str(img_size[2]))
    title.appendChild(title_text)
    size.appendChild(title)

    for i in range(len(boxes)):
        box=boxes[i]
        kp=keypoints[i]

        object =doc.createElement('object')
        annotation.appendChild(object)

        title = doc.createElement('name')
        title_text = doc.createTextNode('parking_empty')
        title.appendChild(title_text)
        object.appendChild(title)

        title = doc.createElement('difficult')
        title_text = doc.createTextNode(str(int(1)))
        title.appendChild(title_text)
        object.appendChild(title)

        # begin bndbox
        bndbox = doc.createElement('bndbox')
        object.appendChild(bndbox)

        title = doc.createElement('xmin')
        title_text = doc.createTextNode(str(int(box[0])))
        title.appendChild(title_text)
        bndbox.appendChild(title)

        title = doc.createElement('ymin')
        title_text = doc.createTextNode(str(int(box[1])))
        title.appendChild(title_text)
        bndbox.appendChild(title)

        title = doc.createElement('xmax')
        title_text = doc.createTextNode(str(int(box[2])))
        title.appendChild(title_text)
        bndbox.appendChild(title)

        title = doc.createElement('ymax')
        title_text = doc.createTextNode(str(int(box[3])))
        title.appendChild(title_text)
        bndbox.appendChild(title)
        #end bndbox
        # keypoint
        keypoint = doc.createElement('keypoints')
        object.appendChild(keypoint)
        for j in range(4):
            title=doc.createElement(f'x{j}')
            title_text=doc.createTextNode(str(int(kp[j][0])))
            title.appendChild(title_text)
            keypoint.appendChild(title)

            title=doc.createElement(f'y{j}')
            title_text=doc.createTextNode(str(int(kp[j][1])))
            title.appendChild(title_text)
            keypoint.appendChild(title)
        #end keypoint

    xmlname=image_name[:-4]
    if not os.path.exists(xml_path):
        os.makedirs(xml_path)

    f = open(os.path.join(xml_path,xmlname) + '.xml', 'w')
    f.write(doc.toprettyxml(indent=''))
    f.close()


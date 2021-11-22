import cv2
import glob
import json
from gen_xml import generate_xml

b=(255,255,0)
g=(0,255,255)
r=(0,0,255)
show=False
#show=True
add_offset=False

def parse_label_json(json_path):
    key_point=[]
    with open(json_path,'r') as data: 
        load_dict=json.load(data)
        shapes=load_dict['shapes']
        for d in shapes:
            kp=[]
            for p in d['points']:
                kp.append([int(p[0]),int(p[1])])
            key_point.append(kp)
    #将关键定移到车位线中心处，默认偏移10个像素
    if add_offset:
        for i in range(len(key_point)):
            key_point[i][0][0]=max(key_point[i][0][0]-10,0)
            key_point[i][0][1]=min(key_point[i][0][1]+10,960)
            key_point[i][1][0]=min(key_point[i][1][0]+10,1280)
            key_point[i][1][1]=min(key_point[i][1][1]+10,960)
            key_point[i][2][0]=min(key_point[i][2][0]+10,1280)
            key_point[i][2][1]=max(key_point[i][2][1]-10,0)
            key_point[i][3][0]=max(key_point[i][3][0]-10,0)
            key_point[i][3][1]=max(key_point[i][3][1]-10,0)
    return key_point

def generate_bbox_by_keypoint(keypoints):
    bndbox=[]
    for kp in keypoints:
        x=[kp[i][0] for i in range(4)]
        y=[kp[i][1] for i in range(4)]
        xmin,ymin=min(x),min(y)
        xmax,ymax=max(x),max(y)
        bndbox.append([xmin,ymin,xmax,ymax])

    return bndbox

def main(file_path,out_path,w,h):
    json_list=glob.glob(file_path+'/*.json')
    for jf in json_list:
        img_path=jf.replace('json','jpg')
        img=cv2.imread(img_path)
        print('json path is:',jf)
        keypoint=parse_label_json(jf)
        boxes=generate_bbox_by_keypoint(keypoint)
        
        img_name=img_path.split('/')[-1]
        if not show:
            generate_xml(img_name,boxes,keypoint,(w,h,3),out_path)

        if show:
            for kk in keypoint:
                cv2.line(img,kk[0],kk[1],g,2)
                cv2.line(img,kk[1],kk[2],g,2)
                cv2.line(img,kk[2],kk[3],g,2)
                cv2.line(img,kk[3],kk[0],g,2)

            for bbox in boxes:
                cv2.rectangle(img,(bbox[0],bbox[1]),(bbox[2],bbox[3]),b,2)
            cv2.imshow(str(img_path),img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()


if __name__ == '__main__':
    file_path='chewei_data'
    out_path='chewei_data_out'
    main(file_path,out_path,1080,1080)

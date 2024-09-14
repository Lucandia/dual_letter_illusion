import cadquery as cq
import streamlit as st
import os
import time
from streamlit_stl import stl_from_file

def letter(let, angle, fontPath=""):
    """Extrude a letter, center it and rotate of the input angle"""
    wp = (cq.Workplane('XZ')
        .text(let, fontsize, extr, fontPath=fontPath, valign='bottom')
        )
    b_box = wp.combine().objects[0].BoundingBox()
    x_shift = -(b_box.xlen/2 + b_box.xmin )
    wp = (wp.translate([x_shift,extr/2,0])
        .rotate((0,0,0),(0,0,1),angle)
        )
    return wp


def dual_text(text1, text2, fontPath='', save='stl', b_h=2, b_pad=2, b_fil_per=0.8, space_per=0.3, export_name='file'):
    """Generate the dual letter illusion from the two text and save it"""
    space = fontsize*space_per # spece between letter
    res = cq.Assembly() # start assembly
    last_ymax = 0
    for ind, ab in enumerate(zip(text1, text2)):
        try:
            a = letter(ab[0], 45, fontPath=fontPath)
            b = letter(ab[1], 135, fontPath=fontPath,)
            a_inter_b = a & b
            b_box = a_inter_b.objects[0].BoundingBox()
            a_inter_b = a_inter_b.translate([0,-b_box.ymin,0])
            if ind:
                a_inter_b = a_inter_b.translate([0,last_ymax + space,0])
            last_ymax = a_inter_b.objects[0].BoundingBox().ymax
            res.add( a_inter_b) # add the intersection to the assebmly
        except:
            last_ymax += space*1.5

    b_box = res.toCompound().BoundingBox() # calculate the bounding box
    # add the base to the assembly
    res.add(cq.Workplane()
            .box(b_box.xlen+b_pad*2, b_box.ylen+b_pad*2, b_h, centered=(1,0,0))
            .translate([0, -b_pad, -b_h])
            .edges('|Z')
            .fillet(b_box.xlen/2*b_fil_per)
            )
    # convert the assemly toa shape and center it
    res = res.toCompound()
    res = res.translate([0, -b_box.ylen/2,0])
    # export the files
    cq.exporters.export(res, f'file_display.stl')
    cq.exporters.export(res, f"{export_name}.{save}")


if __name__ == "__main__":
    for file in os.listdir():
        if 'file' in file:
            try:
                os.remove(file)
            except:
                print(f'Cannot remove file {file}')

    st.title('TextTango: dual text illusion')
    st.write("Generate a custom dual letter illusion, a 3d ambigram! If you like the project put a like on [Printables](https://www.printables.com/it/model/520333-texttango-dual-letter-illusion) or [support me with a coffee](https://www.paypal.com/donate/?hosted_button_id=V4LJ3Z3B3KXRY)! On Printables you can find more info about the project.", unsafe_allow_html=True)
    st.write("The Web App supports all [Google Fonts](https://fonts.google.com/), check them out!", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    # Input type
    with col1:
        text1 = st.text_input('First text', value="STOP")
    with col2:
        text2 = st.text_input('Second text', value="WORK")
    with col3:
        fontsize = st.number_input('Font size', min_value=1, max_value=None, value=20)
        extr = fontsize*2 # extrude letter

    if len(text1) != len(text2):
        st.warning("The two texts don't have the same length, letters in excess will be cut", icon="⚠️")
    if not text1.isupper() or not text2.isupper():
        st.warning("Non-capital letters with different height lead to bad results", icon="⚠️")

    col1, col2, col3 = st.columns(3)
    # Input type 
    font_dir = os.listdir('fonts')
    with col1:
        font_name = st.selectbox('Select font', ['lato'] + sorted(font_dir))
    with col2:
        font_type_list = [f for f in os.listdir('fonts' + os.sep + font_name) if '.ttf' in f and '-' in f]
        # font with explicit type (-bold, -regular, ...)
        if font_type_list:
            font_start_name = font_type_list[0].split('-')[0]
            font_type_list_name = [f.split('-')[1].strip('.ttf') for f in font_type_list]
            font_type = st.selectbox('Font type', sorted(font_type_list_name))
            font_type_pathname = font_start_name + '-' + font_type + '.ttf'
            font_path = 'fonts' + os.sep + font_name + os.sep + font_type_pathname
        else: # font without explicit type
            font_type_list = [f for f in os.listdir('fonts' + os.sep + font_name) if '.ttf' in f]
            font_type = st.selectbox('Font type', sorted(font_type_list))
            font_path = 'fonts' + os.sep + font_name + os.sep + font_type
    with col3:
        space = st.slider('Letters space (%)', 0, 200, step=1, value=30) / 100
    # base parameters
    col1, col2, col3 = st.columns(3)
    with col1:
        b_h = st.slider('Base height', 0.0, fontsize/2, step=0.1, value=1.0)
    with col2:
        b_pad = st.slider('Base Padding', 0.0, fontsize/2, step=0.1, value=2.0)
    with col3:
        b_fil_per = st.slider('Base fillet (%)', 0, 100, step=1, value=80) / 100


    col1, _, _ = st.columns(3)
    with col1:
        out = st.selectbox('Output file type', ['stl', 'step'])
            

    if st.button('Render'):
        start = time.time()
        with st.spinner('Wait for it...'):
            dual_text(text1, text2, fontPath=font_path, save=out, b_h=b_h, b_pad=b_pad, b_fil_per=b_fil_per, space_per=space)
        end = time.time()
        if f'file.{out}' not in os.listdir():
            st.error('The program was not able to generate the mesh.', icon="🚨")
        else:
            st.success(f'Rendered in {int(end-start)} seconds', icon="✅")
            with open(f'file.{out}', "rb") as file:
                btn = st.download_button(
                        label=f"Download {out}",
                        data=file,
                        file_name=f'TextTango_{text1}_{text2}.{out}',
                        mime=f"model/{out}"
                    )
            st.markdown("Post the make [on Printables](https://www.printables.com/it/model/520333-texttango-dual-letter-illusion) to support the project!", unsafe_allow_html=True)
            st.markdown("I am a student who enjoys 3D printing and programming. To support me with a coffee, just [click here!](https://www.paypal.com/donate/?hosted_button_id=V4LJ3Z3B3KXRY)", unsafe_allow_html=True)

            # stl preview
            stl_from_file('file_display.stl')


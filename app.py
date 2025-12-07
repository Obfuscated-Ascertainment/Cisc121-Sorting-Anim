# app.py
import gradio as gr

def parse_list(s):
    # Only allow integers > 0
    vals = []
    for x in s.split(","):
        x = x.strip()
        if x.isdigit():
            val = int(x)
            if val > 0:
                vals.append(val)
    return vals

def draw(arr, highlight=None, split=None):
    if not arr: return "<p>[]</p>"
    maxv = max(arr) or 1
    bars = []
    for i,v in enumerate(arr):
        h = int((v/maxv)*100)
        color = "skyblue"
        if highlight and i in highlight:
            color = "crimson"
        elif split and i in split[0]:
            color = "lightgreen"
        elif split and i in split[1]:
            color = "orange"
        bars.append(f"<div style='width:30px;height:{h}px;margin:2px;background:{color};border:1px solid #333'></div>")
    return f"<div style='height:120px;display:flex;align-items:flex-end;margin:10px'>{''.join(bars)}</div>"

def merge_sort_frames(arr):
    a=arr[:]; frames=[]
    frames.append(draw(a))  # unsorted list

    def snap(highlight=None, split=None):
        frames.append(draw(a, highlight, split))

    def merge(l,m,r):
        L,R=a[l:m+1],a[m+1:r+1];i=j=0;k=l
        while i<len(L) and j<len(R):
            if L[i]<=R[j]:
                a[k]=L[i]; i+=1
            else:
                a[k]=R[j]; j+=1
            snap([k]); k+=1
        while i<len(L): a[k]=L[i]; i+=1; snap([k]); k+=1
        while j<len(R): a[k]=R[j]; j+=1; snap([k]); k+=1

    def sort(l,r):
        if l<r:
            m=(l+r)//2
            left_idx = list(range(l,m+1))
            right_idx = list(range(m+1,r+1))
            snap(split=(left_idx,right_idx))
            sort(l,m); sort(m+1,r); merge(l,m,r)

    if a: sort(0,len(a)-1); frames.append(draw(a))
    return frames

with gr.Blocks() as demo:
    gr.Markdown("## Visualization of Merge Sort (non-positive integers are ignored in the visualization)")
    frames_state=gr.State([])
    inp=gr.Textbox(label="List",placeholder="e.g. 5,3,8,1")
    slider=gr.Slider(minimum=0,maximum=0,step=1,value=0,label="Step")
    frame=gr.HTML()
    status=gr.Markdown()

    def on_submit(user_input):
        arr=parse_list(user_input)
        if not arr:
            return [],gr.update(minimum=0,maximum=0,value=0),"<p>Please enter integers greater than 0.</p>","No valid input"
        frames=merge_sort_frames(arr)
        return frames,gr.update(minimum=0,maximum=len(frames)-1,value=0),frames[0],f"{len(frames)} frames"

    def on_change(frames,step):
        if not frames: return "<p>No frames</p>","Submit a list first"
        idx=max(0,min(step,len(frames)-1))
        return frames[idx],f"Step {idx+1}/{len(frames)}"

    inp.submit(on_submit,inp,[frames_state,slider,frame,status])
    slider.change(on_change,[frames_state,slider],[frame,status])

demo.launch()

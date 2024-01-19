from tkinter import filedialog,StringVar
import sys
from customtkinter import *
from pytube import YouTube,Playlist
import os

import sys
if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS2'):
    print('running in a PyInstaller bundle')
else:
    print('running in a normal Python process')

class Windows(CTk):
    def window_setup(self):
        self._set_appearance_mode('dark')
        self._set_appearance_mode('green')
        self.geometry('760x480')
        self.title('YOUTUBE VIDEO DOWNLOADER')     
        self.minsize(720,480)


def bytes_to_mb(bytes):
    mb = round((bytes/(1024*1024)),2)
    return mb 


# CREATING OUR WINDOW OBJECT
app = Windows()
app.window_setup()

# CREATING TABS FOR SWITCHING BETWEEN SINGLE AND MUTLIPLE VIDEO DOWNLOADER
tabs = CTkTabview(app,width=695,height=450)
tabs.pack(fill=BOTH,expand=TRUE,padx=10,pady=10)

single_video_tab = tabs.add('SINGLE VIDEO')
multiple_video_tab = tabs.add('MULTIPLE VIDEOS')
playlist_video_tab = tabs.add('PLAYLIST VIDEOS')
buy_me_garri = tabs.add('BUY ME GARRI')

# A FUNCTION TO MANAGE EVERYTHING ABOUT SINGLE VIDEO DOWNLOADER
def single_video_downloader(tab):
    def start_download(resolution_option):
        try:
            link = link_variable.get()
            ytObject = YouTube(link,on_progress_callback=on_progress)

            # Download the video
            if resolution_option.lower() == '360p':
                resolution.set('360P')
                ytvideo = ytObject.streams.get_lowest_resolution()
            elif resolution_option.lower() == '720p':
                resolution.set('720P')
                ytvideo = ytObject.streams.get_highest_resolution()
            else:
                print("error")
            path = filedialog.askdirectory()
            ytvideo = ytvideo.download(output_path=path)
            resolution.pack_forget()
            place_holder1.configure(text='DOWNLOAD COMPLETED😊',text_color=('green'))
                
        except Exception as e:
            place_holder1.configure(text=f'Error downloading video, {e}',text_color='red')


    def on_progress(stream,chunk,bytes_remaining):
        total_size = stream.filesize
        size_downloaded = total_size - bytes_remaining
        percentage_of_completion = ((size_downloaded/total_size)*100)
        per = str(int(percentage_of_completion))
        progress_percentage.configure(text=f'{per}%')
        progress_percentage.update()
        #updating the progress bar
        progress_bar.set(float(percentage_of_completion)/100)


    def get_info():
        # try:
        link = link_variable.get()
        ytObject = YouTube(url=link)
        # title = ytObject.title
        # label.configure(text=title,text_color='Grey')
        highest_resolution_filesize = bytes_to_mb(ytObject.streams.get_highest_resolution().filesize)
        lowest_resoltion_filesize = bytes_to_mb(ytObject.streams.get_lowest_resolution().filesize)
        place_holder1.configure(text=f'360P: {lowest_resoltion_filesize}mb              720P: {highest_resolution_filesize}mb',text_color='green')
        resolution.set('Choose Resolution')
        resolution.pack()    

            
        # except Exception as e:
        #     place_holder1.configure(text=f'Input a valid link or check your internet connection!!!!, {e}',text_color='red')


    # creating WELCOME MESSAGE 
    label = CTkLabel(tab,text=f'INSERT YOUTUBE LINK TO GET VIDEO TITLE 👇',font=('Helvetica',18))
    label.pack(padx=10,pady=20)

    # CREATING AN ENTRY FIELD TO ENTER LINK
    link_variable = StringVar()
    link_entry_widget = CTkEntry(tab,width=500,placeholder_text='input youtube video link here 👇',placeholder_text_color='white',border_color='light blue',textvariable=link_variable)
    link_entry_widget.pack(padx=10,pady=10)

    #PLACE HOLDER LABELS FOR DISPLAYING WHAT WE WANT
    place_holder1 = CTkLabel(tab, text ='')
    place_holder1.pack()

    # CREATING PERCENTAGE AND PROGRESS BAR
    progress_percentage = CTkLabel(tab,text='0%')
    progress_percentage.pack()
    progress_bar = CTkProgressBar(tab,width=400,progress_color='lightblue')
    progress_bar.set(0)
    progress_bar.pack()

    #CREATING COMBO BOX FOR RESOLUTION
    resolutions_available = ('360P','720P')
    resolution =  CTkComboBox(tab,values=resolutions_available,command=start_download)
    resolution_option = str(resolution)

    # CREATING A GET INFORMATION BUTTON
    info_button = CTkButton(tab,border_width=2,border_color='light blue',text='GET VIDEO INFO',command=get_info)
    info_button.pack(padx=10,pady=10)


# FUNCTION TO MANAGE THE MULTIPLE VIDEO DOWNLOADER TAB
def multiple_video_downloader(tab):
    def count_urls(urls):
        count = 0
        links = []
        for url in urls:
            url = url.strip()
            if 'youtube' in url:
                links.append(url)
                count += 1
        return count,links

    def start_download(resolution_option):
        try:
            file = text_file.get()
            urls = open(file,'r')
            total_count,ytlinks = count_urls(urls)
            count = 0
            path = filedialog.askdirectory()
            for url in ytlinks:
                ytObject = YouTube(url,on_progress_callback=on_progress)
                title = ytObject.title
                current_video_title.configure(text=title)
                if resolution_option.lower() == '360p':
                    resolution.set('360P')
                    ytvideo = ytObject.streams.get_lowest_resolution()
                elif resolution_option.lower() == '720p':
                    resolution.set('720P')
                    ytvideo = ytObject.streams.get_highest_resolution()
                else:
                    pass
                ytvideo.download(output_path=path)
                count += 1
                percentage_of_file_downloaded = (count/total_count)
                file_progress_bar.set(percentage_of_file_downloaded)  
                video_title.configure(text=f'Downloaded {count} videos out of {total_count}')
                    
            place_holder_label.configure(text='DOWNLOAD COMPLETED😊',text_color=('green'))
            resolution.pack_forget()

        except Exception as e:
            place_holder_label.configure(text=f'ERROR DOWNLOADING VIDEO, CHECK YOUR INTERNET CONNECTION!!!!!, {e}',text_color='red')    

    # UPDATING PROGRESS BAR FOR CURRENT VIDEO DOWNLOADING....
    def on_progress(stream,chunk,bytes_remaining):
        total_size = stream.filesize
        size_downloaded = total_size - bytes_remaining
        percentage_of_completion = ((size_downloaded/total_size)*100)
        per = str(int(percentage_of_completion))
        progress_percentage.configure(text=f'{per}%')
        progress_percentage.update()
        #updating the progress bar
        video_progressbar.set(float(percentage_of_completion)/100)


    def get_info():
        try:
            count = 0
            urls = filedialog.askopenfile('r',initialdir='C:/',filetypes=(("text files","*.txt"), ("all files", "*")))
            high_resolution_filesize = 0
            low_resolution_filesize = 0
            for url in urls:                
                url = url.strip()
                if 'youtube' in url:
                    ytObject = YouTube(url=url)
                    highest_resolution_filesize = bytes_to_mb(ytObject.streams.get_highest_resolution().filesize)
                    lowest_resolution_filesize = bytes_to_mb(ytObject.streams.get_lowest_resolution().filesize)
                    low_resolution_filesize += round(lowest_resolution_filesize,2)
                    high_resolution_filesize += highest_resolution_filesize
                    count += 1
            
            place_holder_label.configure(text=f'360P: {low_resolution_filesize}mb              720P: {high_resolution_filesize}mb',text_color='green')
            video_title.configure(text=f'There are {count} videos presently in your file  ',text_color='Grey')
            current_video_title.configure(text = 'INSERT TEXT FILE TO EXTRACT MULTIPLE VIDEO URL')
            progress_percentage.configure(text='0%')
            video_progressbar.set(0)
            file_progress_bar.set(0)
            
            resolution.set('Choose Resolution')
            resolution.pack()
            
        except Exception as e:
            place_holder_label.configure(text=f'Input a text file directory, check your directory and try again later!!!!, \n{e}',text_color='red')
            video_title.configure(text=' ')

    # VIDEO TITLE
    current_video_title = CTkLabel(tab,text='INSERT TEXT FILE TO EXTRACT MULTIPLE VIDEO URL 👇',font=('Helvetica',18))
    current_video_title.pack(padx=10,pady=10)

    #VIDEO BEING DOWNLOADED TITLE
    video_title = CTkLabel(tab,text=' ',text_color='lightblue')
    video_title.pack(pady=10)

    # PLAYLIST LINK ENTRY
    text_file = StringVar()
    text_file_entry = CTkLabel(tab,text=' ', font=('Helvica',16))
    text_file_entry.pack()

    # RESOLUTION LABEL/STATUS
    place_holder_label = CTkLabel(tab,text='',text_color='green')
    place_holder_label.pack(padx=10,pady=10)
    
    #VIDEO PROGRESS BAR
    progress_percentage = CTkLabel(tab,text='0%')
    video_progressbar = CTkProgressBar(tab,width=350,progress_color='lightblue')
    video_progressbar.set(0)

    # FILE AND VIDEO PROGRESS BAR
    file_progress_bar = CTkProgressBar(tab,width=500,progress_color='green')
    file_progress_bar.set(0)

    progress_percentage.pack()
    video_progressbar.pack()
    file_progress_bar.pack(padx=10,pady=10)

    #BUTTONS
    get_info_button = CTkButton(tab,border_width=2,border_color='light blue',text='GET FILE INFO',command=get_info)
    get_info_button.pack(padx=10,pady=10)

    resolutions_available = ('360P','720P')
    resolution =  CTkComboBox(tab,values=resolutions_available,command=start_download)
    resolution_option = str(resolution)


def playlist_videos_downloader(tab):
    def count_urls(urls):
        count = 0
        links = []
        for url in urls:
            url = url.strip()
            if 'youtube' in url:
                links.append(url)
                count += 1
        return count,links

    def start_download(resolution_option):
        try:
            playlist_url = playlist_link.get()
            playlistObject = Playlist(playlist_url)
            total_count,ytlinks = count_urls(playlistObject)
            count = 0
            path = filedialog.askdirectory()
            for url in ytlinks:
                ytObject = YouTube(url,on_progress_callback=on_progress)
                title = ytObject.title
                current_video_title.configure(text=title)
                if resolution_option.lower() == '360p':
                    resolution.set('360P')
                    ytvideo = ytObject.streams.get_lowest_resolution()
                elif resolution_option.lower() == '720p':
                    resolution.set('720P')
                    ytvideo = ytObject.streams.get_highest_resolution()
                else:
                    pass
                ytvideo.download(output_path=path)
                count += 1
                percentage_of_file_downloaded = (count/total_count)
                file_progress_bar.set(percentage_of_file_downloaded)  
                video_title.configure(text=f'Downloaded {count} videos out of {total_count}')
                    
            place_holder_label.configure(text='DOWNLOAD COMPLETED😊',text_color=('green'))
            resolution.pack_forget()

        except Exception as e:
            place_holder_label.configure(text=f'ERROR DOWNLOADING VIDEO, CHECK YOUR INTERNET CONNECTION!!!!!, {e}',text_color='red')    

    # UPDATING PROGRESS BAR FOR CURRENT VIDEO DOWNLOADING....
    def on_progress(stream,chunk,bytes_remaining):
        total_size = stream.filesize
        size_downloaded = total_size - bytes_remaining
        percentage_of_completion = ((size_downloaded/total_size)*100)
        per = str(int(percentage_of_completion))
        progress_percentage.configure(text=f'{per}%')
        #updating the progress bar
        video_progressbar.set(float(percentage_of_completion)/100)
        progress_percentage.update()
        


    def get_info():
        try:
            count = 0
            playlist_url = playlist_link.get()
            playlistObject = Playlist(playlist_url)
            title = str(playlistObject.title).upper()
            playlist_title.configure(text=title)
            total_high_resolution_filesize = 0
            total_low_resolution_filesize = 0
            for url in playlistObject.video_urls:                
                url = url.strip()
                if 'youtube' in url:
                    ytObject = YouTube(url=url)
                    highest_resolution_filesize = bytes_to_mb(ytObject.streams.get_highest_resolution().filesize)
                    lowest_resolution_filesize = bytes_to_mb(ytObject.streams.get_lowest_resolution().filesize)
                    total_low_resolution_filesize += round(lowest_resolution_filesize,2)
                    total_high_resolution_filesize += highest_resolution_filesize
                    count += 1
            
            place_holder_label.configure(text=f'360P: {total_low_resolution_filesize}mb              720P: {total_high_resolution_filesize}mb',text_color='green')
            video_title.configure(text=f'There are {count} videos presently in this playlist  ',text_color='Grey')
            current_video_title.configure(text = 'INSERT TEXT FILE TO EXTRACT MULTIPLE VIDEO URL')
            progress_percentage.configure(text='0%')
            video_progressbar.set(0)
            file_progress_bar.set(0)
            
            resolution.set('Choose Resolution')
            resolution.pack()
            
        except Exception as e:
            place_holder_label.configure(text=f'INPUT A VALID YOUTUBE PLAYLIST LINK/URL and try again!!!!, \n{e}',text_color='red')
            video_title.configure(text=' ')

    # PLAYLIST TITLE
    playlist_title = CTkLabel(tab,text=' ',font=('Helvetica',16))
    
    # VIDEO TITLE
    current_video_title = CTkLabel(tab,text='INSERT PLAYLIST URL TO EXTRACT PLAYLIST VIDEOS URL 👇',font=('Helvetica',14))
    current_video_title.pack(padx=10,pady=10)
    playlist_title.pack()

    #VIDEO BEING DOWNLOADED TITLE
    video_title = CTkLabel(tab,text=' ',text_color='lightblue')
    video_title.pack(pady=10)

    # PLAYLIST LINK ENTRY
    playlist_link = StringVar()
    playlist_link_entry = CTkEntry(tab,width=500,placeholder_text='ENTER PLAYLIST URL 👇',placeholder_text_color='white',border_color='lightblue',textvariable=playlist_link)
    playlist_link_entry.pack()

    # RESOLUTION LABEL/STATUS
    place_holder_label = CTkLabel(tab,text='',text_color='green')
    place_holder_label.pack(padx=10,pady=10)
    
    #VIDEO PROGRESS BAR
    progress_percentage = CTkLabel(tab,text='0%')
    video_progressbar = CTkProgressBar(tab,width=350,progress_color='lightblue')
    video_progressbar.set(0)

    # FILE AND VIDEO PROGRESS BAR
    file_progress_bar = CTkProgressBar(tab,width=500,progress_color='green')
    file_progress_bar.set(0)

    progress_percentage.pack()
    video_progressbar.pack()
    file_progress_bar.pack(padx=10,pady=10)

    #BUTTONS
    get_info_button = CTkButton(tab,border_width=2,border_color='light blue',text='GET TEXT FILE',command=get_info)
    get_info_button.pack(padx=10,pady=10)

    resolutions_available = ('360P','720P')
    resolution =  CTkComboBox(tab,values=resolutions_available,command=start_download)
    resolution_option = str(resolution)

# A TAB TO ASK FOR SUPPORT
def about(tab):
    credits = CTkLabel(tab, text= '''
                    
If you find this GUI useful or encounter any problem feel free to contact us on: 08110265470
                       
If you really liked our program and wish to buy us garri👇:
                    
7045101870 
Opay 
Stephen Oshateye. ''',font=('Helvetica',16))
    credits.pack(padx=10,pady=10)

single_video_downloader(single_video_tab)
multiple_video_downloader(multiple_video_tab)
playlist_videos_downloader(playlist_video_tab)
about(buy_me_garri)
# keeping our app running
app.mainloop() 
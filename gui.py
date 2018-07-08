#TODO:
# change things (including stop simulation)
# speed/delay
try:
	import tkinter
except ImportError:
	import Tkinter as tkinter
import tkinter.messagebox
import model
import modelview
import modelhistory
import modelhistoryview
import threading
from time import sleep

has_setup_view = None

top = tkinter.Tk()
top.title("Hoax spread model")

def isNaturalNumber(input):
	if input =='':
		return True
	try:
		val = int(input)
		if val < 0:
			return False
		return True
	except ValueError:
		return False

def isBetween01(input):
	if input =='':
		return True
	try:
		val = float(input)
		if val < 0:
			return False
		elif val > 1:
			return False
		return True
	except ValueError:
		return False

naturalNumberValidateCommand =  top.register(isNaturalNumber)
between01ValidateCommand =  top.register(isBetween01)

# add widgets
n_label_text = tkinter.StringVar()
n_label_text.set("number of nodes:")
n_label = tkinter.Label(top, textvariable=n_label_text)
n_label.grid(row=0)
n_entry = tkinter.Entry(top,width=5,validate="all",validatecommand=(naturalNumberValidateCommand,'%P'))
n_entry.grid(row=0, column=1)
n_entry.insert(0, "100")

k_label_text = tkinter.StringVar()
k_label_text.set("k:")
k_label = tkinter.Label(top, textvariable=k_label_text)
k_label.grid(row=0, column=2)
k_entry = tkinter.Entry(top,width=5,validate="all",validatecommand=(naturalNumberValidateCommand,'%P'))
k_entry.grid(row=0, column=3)
k_entry.insert(0, "6")

network_type_label_text = tkinter.StringVar()
network_type_label_text.set("network type:")
network_type_label = tkinter.Label(top, textvariable=network_type_label_text)
network_type_label.grid(row=1)
network_type_var = tkinter.StringVar()
network_type_var.set("barabasi-albert")
network_type_optionmenu = tkinter.OptionMenu(top,network_type_var,"barabasi-albert","erdos-renyi")
network_type_optionmenu.grid(row=1, column=1)

initial_outbreak_label_text = tkinter.StringVar()
initial_outbreak_label_text.set("initial outbreak:")
initial_outbreak_label = tkinter.Label(top, textvariable=initial_outbreak_label_text)
initial_outbreak_label.grid(row=1, column=2)
initial_outbreak_entry = tkinter.Entry(top,width=5,validate="all",validatecommand=(naturalNumberValidateCommand,'%P'))
initial_outbreak_entry.grid(row=1, column=3)
initial_outbreak_entry.insert(0, "6")

layout_var = tkinter.BooleanVar()
layout_var.set(False)
layout_checkbutton = tkinter.Checkbutton(top, text="layout", variable = layout_var)
layout_checkbutton.grid(row=2,column=0)

def setup_network_callback():
	global has_setup_view
	model.setup_network(network_type_var.get(),int(n_entry.get()),int(k_entry.get()),int(initial_outbreak_entry.get()))
	modelhistory.reset()
	if show_current_network_var.get():
		modelview.setup_view(layout_var.get())
		modelview.update_view()
		has_setup_view=True
	else:
		has_setup_view=False
	modelhistoryview.update_view()

setup_network_button = tkinter.Button(top, text="setup network", command=setup_network_callback)
setup_network_button.grid(row=2, column=1)

n_clr_buzz_label_text = tkinter.StringVar()
n_clr_buzz_label_text.set("number of clarifying buzzers:")
n_clr_buzz_label = tkinter.Label(top, textvariable=n_clr_buzz_label_text)
n_clr_buzz_label.grid(row=3, column=0)
n_clr_buzz_entry = tkinter.Entry(top,width=5,validate="all",validatecommand=(naturalNumberValidateCommand,'%P'))
n_clr_buzz_entry.grid(row=3, column=1)
n_clr_buzz_entry.insert(0, "0")

n_hoax_buzz_label_text = tkinter.StringVar()
n_hoax_buzz_label_text.set("number of hoax buzzers:")
n_hoax_buzz_label = tkinter.Label(top, textvariable=n_hoax_buzz_label_text)
n_hoax_buzz_label.grid(row=3, column=2)
n_hoax_buzz_entry = tkinter.Entry(top,width=5,validate="all",validatecommand=(naturalNumberValidateCommand,'%P'))
n_hoax_buzz_entry.grid(row=3, column=3)
n_hoax_buzz_entry.insert(0, "0")

clr_strategy_label_text = tkinter.StringVar()
clr_strategy_label_text.set("clarifying buzzer placement:")
clr_strategy_label = tkinter.Label(top, textvariable=clr_strategy_label_text)
clr_strategy_label.grid(row=4)
clr_strategy_var = tkinter.StringVar()
clr_strategy_var.set("supernodes")
clr_strategy_optionmenu = tkinter.OptionMenu(top,clr_strategy_var,"supernodes","random","peripheral")
clr_strategy_optionmenu.grid(row=4, column=1)

hoax_strategy_label_text = tkinter.StringVar()
hoax_strategy_label_text.set("hoax buzzer placement:")
hoax_strategy_label = tkinter.Label(top, textvariable=hoax_strategy_label_text)
hoax_strategy_label.grid(row=4, column=2)
hoax_strategy_var = tkinter.StringVar()
hoax_strategy_var.set("supernodes")
hoax_strategy_optionmenu = tkinter.OptionMenu(top,hoax_strategy_var,"supernodes","random","peripheral")
hoax_strategy_optionmenu.grid(row=4, column=3)

placement_threshold_label_text = tkinter.StringVar()
placement_threshold_label_text.set("placement threshold:")
placement_threshold_label = tkinter.Label(top, textvariable=placement_threshold_label_text)
placement_threshold_label.grid(row=5, column=0)
placement_threshold_entry = tkinter.Entry(top,width=5,validate="all",validatecommand=(between01ValidateCommand,'%P'))
placement_threshold_entry.grid(row=5, column=1)
placement_threshold_entry.insert(0, "0.05")

has_setup_buzzers_view = None
def setup_buzzers_callback():
	global has_setup_view, has_setup_buzzers_view
	if modelhistory.ticks is None:
		tkinter.messagebox.showerror("Error","Setup network first")
		return None
	model.setup_buzzers(int(n_clr_buzz_entry.get()), clr_strategy_var.get(), int(n_hoax_buzz_entry.get()), hoax_strategy_var.get(), float(placement_threshold_entry.get()))
	modelhistory.reset()
	if show_current_network_var.get():
		if not has_setup_view:
			modelview.setup_view()
			setup_view = True
		modelview.setup_buzzers_view()
		has_setup_buzzers_view = True
		modelview.update_view()
	else:
		has_setup_buzzers_view = False
	modelhistoryview.update_view()

setup_buzzers_button = tkinter.Button(top, text="setup buzzers", command=setup_buzzers_callback)
setup_buzzers_button.grid(row=5, column=2)

separator_label_text = tkinter.StringVar()
separator_label_text.set("=================")
separator_label = tkinter.Label(top, textvariable=separator_label_text)
separator_label.grid(row=6,column=1, columnspan=2)

spread_chance_label_text = tkinter.StringVar()
spread_chance_label_text.set("spread chance:")
spread_chance_label = tkinter.Label(top, textvariable=spread_chance_label_text)
spread_chance_label.grid(row=7, column=1)
spread_chance_entry = tkinter.Entry(top,width=5,validate="all",validatecommand=(between01ValidateCommand,'%P'))
spread_chance_entry.grid(row=7, column=2)
spread_chance_entry.insert(0, "0.5")

hoax_believability_label_text = tkinter.StringVar()
hoax_believability_label_text.set("hoax believability:")
hoax_believability_label = tkinter.Label(top, textvariable=hoax_believability_label_text)
hoax_believability_label.grid(row=8, column=1)
hoax_believability_entry = tkinter.Entry(top,width=5,validate="all",validatecommand=(between01ValidateCommand,'%P'))
hoax_believability_entry.grid(row=8, column=2)
hoax_believability_entry.insert(0, "0.6")

iv_chance_label_text = tkinter.StringVar()
iv_chance_label_text.set("induced verification chance:")
iv_chance_label = tkinter.Label(top, textvariable=iv_chance_label_text)
iv_chance_label.grid(row=9, column=1)
iv_chance_entry = tkinter.Entry(top,width=5,validate="all",validatecommand=(between01ValidateCommand,'%P'))
iv_chance_entry.grid(row=9, column=2)
iv_chance_entry.insert(0, "0.06")

bf_chance_label_text = tkinter.StringVar()
bf_chance_label_text.set("backfire chance:")
bf_chance_label = tkinter.Label(top, textvariable=bf_chance_label_text)
bf_chance_label.grid(row=10, column=1)
bf_chance_entry = tkinter.Entry(top,width=5,validate="all",validatecommand=(between01ValidateCommand,'%P'))
bf_chance_entry.grid(row=10, column=2)
bf_chance_entry.insert(0, "0.08")

vv_chance_label_text = tkinter.StringVar()
vv_chance_label_text.set("voluntary verification chance:")
vv_chance_label = tkinter.Label(top, textvariable=vv_chance_label_text)
vv_chance_label.grid(row=11, column=1)
vv_chance_entry = tkinter.Entry(top,width=5,validate="all",validatecommand=(between01ValidateCommand,'%P'))
vv_chance_entry.grid(row=11, column=2)
vv_chance_entry.insert(0, "0.02")

f_chance_label_text = tkinter.StringVar()
f_chance_label_text.set("forget chance:")
f_chance_label = tkinter.Label(top, textvariable=f_chance_label_text)
f_chance_label.grid(row=12, column=1)
f_chance_entry = tkinter.Entry(top,width=5,validate="all",validatecommand=(between01ValidateCommand,'%P'))
f_chance_entry.grid(row=12, column=2)
f_chance_entry.insert(0, "0.10")

def try_show_current_network():
	global has_setup_view, has_setup_buzzers_view
	if show_current_network_var.get():
		if not has_setup_view:
			modelview.setup_view()
			has_setup_view = True
		if not has_setup_buzzers_view:
			modelview.setup_buzzers_view()
			has_setup_buzzers_view = True
		modelview.update_view()

def go_once_callback():
	if modelhistory.ticks is None:
		tkinter.messagebox.showerror("Error","Setup network first")
		return None
	model.go(float(spread_chance_entry.get()),float(hoax_believability_entry.get()),float(f_chance_entry.get()),float(vv_chance_entry.get()),float(iv_chance_entry.get()),float(bf_chance_entry.get()))
	modelhistory.tick()
	try_show_current_network()
	modelhistoryview.update_view()

go_once_button = tkinter.Button(top, text="go once", command=go_once_callback)
go_once_button.grid(row=13, column=0)

stop_at_label_text = tkinter.StringVar()
stop_at_label_text.set("stop at:")
stop_at_label = tkinter.Label(top, textvariable=stop_at_label_text)
stop_at_label.grid(row=13, column=2)
stop_at_entry = tkinter.Entry(top,width=5,validate="all",validatecommand=(naturalNumberValidateCommand,'%P'))
stop_at_entry.grid(row=13, column=3)
stop_at_entry.insert(0, "500")

go_repeat_done = None
stop_at = None
spread_chance = None
hoax_believability = None
f_chance = None
vv_chance = None
iv_chance = None
bf_chance = None

def go_repeat_worker():
	global go_repeat_done
	if modelhistory.ticks <= stop_at:
		model.go(spread_chance,hoax_believability,f_chance,vv_chance,iv_chance,bf_chance)
		modelhistory.tick()
		async_jobs.append(go_repeat_worker)
	else:
		go_repeat_done = True

def go_repeat_callback():
	global go_repeat_done, async_jobs, stop_at, spread_chance, hoax_believability, vv_chance, iv_chance, bf_chance, f_chance
	if modelhistory.ticks is None:
		tkinter.messagebox.showerror("Error","Setup network first")
		return None
	go_repeat_done = False
	stop_at = int(stop_at_entry.get())
	spread_chance = float(spread_chance_entry.get())
	hoax_believability = float(hoax_believability_entry.get())
	f_chance = float(f_chance_entry.get())
	vv_chance = float(vv_chance_entry.get())
	iv_chance = float(iv_chance_entry.get())
	bf_chance = float(bf_chance_entry.get())
	async_jobs.append(go_repeat_worker)
	while not go_repeat_done:
		try:
			try_show_current_network()
			modelhistoryview.update_view()
		except ValueError:
			pass
		except tkinter._tkinter.TclError:
			async_jobs.append(destroy_all_jobs_job)

go_repeat_button = tkinter.Button(top, text="go repeat", command=go_repeat_callback)
go_repeat_button.grid(row=13, column=1)

def destroy_all_jobs_job():
	del async_jobs[:]

is_running = True
async_jobs = []
def async_job_worker(idledelayseconds):
	while is_running:
		if not async_jobs:
			sleep(idledelayseconds)
		else:
			current_job = async_jobs.pop(0)
			current_job()

async_job_thread = threading.Thread(target = async_job_worker, args = (1, ))
async_job_thread.start()

show_current_network_var = tkinter.BooleanVar()
show_current_network_var.set(False)
show_current_network_checkbutton = tkinter.Checkbutton(top, text="show current network", variable = show_current_network_var)
show_current_network_checkbutton.grid(row=14,column=1)

top.mainloop()
is_running = False
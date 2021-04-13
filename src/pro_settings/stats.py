import numpy
FOLDER = "C:\\Users\\Rodio\\Desktop\\Workspaces\\sens_master\\src\\"

def get_csv(file):
    return numpy.genfromtxt(FOLDER + file, delimiter=',')

fortnite_x_sens = get_csv('fortnite_x_sens.csv')
fortnite_y_sens = get_csv('fortnite_y_sens.csv')
fortnite_x_sens_targeting = get_csv('fortnite_x_sens_targeting.csv')
fortnite_y_sens_targeting = get_csv('fortnite_y_sens_targeting.csv')
fortnite_x_sens_scoped = get_csv('fortnite_x_sens_scoped.csv')
fortnite_y_sens_scoped = get_csv('fortnite_y_sens_scoped.csv')
val_sens = get_csv('val_sens.csv')
csgo_sens = get_csv('csgo_sens.csv')
ow_sens = get_csv('ow_sens.csv')
al_sens = get_csv('al_sens.csv')
master_sens = numpy.concatenate((fortnite_x_sens, val_sens, csgo_sens, ow_sens, al_sens))

def stat_info_str(arr):
    out = str("Q1: {:.2f}\nQ2: {:.2f}\nQ3: {:.2f}\nAV: {:.2f}\n\n".format(
        numpy.percentile(arr, 25),
        numpy.percentile(arr, 50),
        numpy.percentile(arr, 75),
        numpy.average(arr)))
    return out

file_content = (
    "csgo_sens\n" +
    stat_info_str(csgo_sens) +
    "val_sens\n" + 
    stat_info_str(val_sens) +
    "ow_sens\n" + 
    stat_info_str(ow_sens) +
    "al_sens\n" + 
    stat_info_str(al_sens) +
    "fortnite_x_sens\n" +
    stat_info_str(fortnite_x_sens) + 
    "fortnite_y_sens\n" +
    stat_info_str(fortnite_y_sens) + 
    "fortnite_x_sens_targeting\n" +
    stat_info_str(fortnite_x_sens_targeting) + 
    "fortnite_y_sens_targeting\n" +
    stat_info_str(fortnite_y_sens_targeting) +
    "fortnite_x_sens_scoped\n" +
    stat_info_str(fortnite_x_sens_scoped) +
    "fortnite_y_sens_scoped\n" +
    stat_info_str(fortnite_y_sens_scoped) +
    "master_sens\n" +
    stat_info_str(master_sens)
)

f = open("sens_stats.txt", "w")
f.write(file_content)
f.close()
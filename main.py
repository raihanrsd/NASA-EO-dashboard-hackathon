from simpleimage import SimpleImage
import seaborn as sns
import matplotlib.pyplot as plt
import csv
import json


def main():
    intensity = 1.5
    query = input("Which city social trend analysis do you want?(click enter to end) ")
    query_dict = {
        "Beijing": "given city",
        "Washington": "given city",
        "Gent port": "given city",
    }
    while query != "":
        if query_dict.get(query) != None:
            slowdown = slowdown_analysis(query + "_slowdown.png", intensity)
            recovery = recovery_analysis(query + "_recovery.png", intensity)
            region_dict = region_analysis(
                query + "_slowdown.png", query + "_recovery.png", intensity
            )
            recovery_sign = recovery - slowdown
            recovery_rate = (recovery_sign / slowdown) * 100
            region_dict[query] = float(recovery_rate)
            make_bar_plot(region_dict)
            print(region_dict)
            print("")
            print(
                "The recovery rate in "
                + query
                + " is "
                + str(recovery_rate)
                + "% more than the slowdown rate."
            )
            get_response(float(recovery_rate))
        else:
            print("Please provide a valid input.")
        query = input(
            "Which city social trend analysis do you want?(click enter to end) "
        )

    print("The program has ended.")


def slowdown_analysis(imagefile, intensity):
    slowdown_image = SimpleImage(imagefile)
    slowdown_image.show()
    pics_num = 0
    pics_blue = 0

    for pixel in slowdown_image:
        pics_num += 1
        if ((pixel.red + pixel.blue + pixel.green) // 3) * intensity < pixel.blue:
            pics_blue += 1

    percentage_area_slowdown = (pics_blue / pics_num) * 100
    print("Number of blue pixels are " + str(pics_blue))
    print("Total number of Pixel are " + str(pics_num))
    print("Percentage of area slowed down " + str(percentage_area_slowdown) + "%")
    return percentage_area_slowdown


def region_analysis(slowdown, recovery, intensity):
    slowdown = SimpleImage(slowdown)
    recovery = SimpleImage(recovery)
    region_dict = {
        0: {0: "North-West", 1: "West", 2: "South-West"},
        1: {0: "North", 1: "Central", 2: "South"},
        2: {0: "North-East", 1: "East", 2: "South-East"},
    }
    region_stats = {}
    for i in range(3):
        for j in range(3):
            region_stats[region_dict[i][j]] = get_region_stats(
                i, j, slowdown, recovery, intensity, region_dict
            )
    print(region_stats)
    return region_stats


def get_region_stats(i, j, slowdown, recovery, intensity, region):

    region_slowdown_part = SimpleImage.blank(slowdown.width // 3, slowdown.height // 3)
    for x in range(region_slowdown_part.width):
        for y in range(region_slowdown_part.height):
            pixel = slowdown.get_pixel(
                x + (slowdown.width // 3) * i, y + (slowdown.height // 3) * j
            )
            region_slowdown_part.set_pixel(x, y, pixel)
    region_slowdown_part.show()
    pics_num = 0
    pics_blue = 0

    for pixel in region_slowdown_part:
        pics_num += 1
        if ((pixel.red + pixel.blue + pixel.green) // 3) * intensity < pixel.blue:
            pics_blue += 1
    percentage_area_slowdown = (pics_blue / pics_num) * 100

    region_recovery_part = SimpleImage.blank(recovery.width // 3, recovery.height // 3)
    for x in range(region_recovery_part.width):
        for y in range(region_recovery_part.height):
            pixel = recovery.get_pixel(
                x + (recovery.width // 3) * i, y + (recovery.height // 3) * j
            )
            region_recovery_part.set_pixel(x, y, pixel)
    region_recovery_part.show()
    pics_num1 = 0
    pics_yellow = 0

    for pixel in region_recovery_part:
        pics_num1 += 1
        if pixel.red > ((pixel.blue + pixel.green) // 2) * intensity:
            pics_yellow += 1

    percentage_area_recovery = (pics_yellow / pics_num1) * 100

    recovery_sign = percentage_area_recovery - percentage_area_slowdown
    recovery_rate = (recovery_sign / percentage_area_slowdown) * 100
    print("")
    print(
        "The recovery rate in "
        + region[i][j]
        + " part is "
        + str(recovery_rate)
        + "% more than the slowdown rate."
    )
    get_response(float(recovery_rate))
    return float(recovery_rate)


def recovery_analysis(imagefile, intensity):
    recovery_image = SimpleImage(imagefile)
    recovery_image.show()
    pics_num1 = 0
    pics_yellow = 0

    for pixel in recovery_image:
        pics_num1 += 1
        if pixel.red > ((pixel.blue + pixel.green) // 2) * intensity:
            pics_yellow += 1

    percentage_area_recovery = (pics_yellow / pics_num1) * 100
    print("Number of yellow pixels are " + str(pics_yellow))
    print("Total number of Pixel are " + str(pics_num1))
    print("Percentage of area recovered " + str(percentage_area_recovery) + "%")
    return percentage_area_recovery


def make_bar_plot(count_map):
    """
    Turns a dictionary (where values are numbers) into a bar plot.
    Labels gives the order of the bars! Uses a package called seaborn
    for making graphs.
    """
    # turn the counts into a list
    counts = []
    # loop over the labels, in order
    for label in count_map:
        counts.append(count_map[label])
    # format the data in the way that seaborn wants
    data = {"x": list(count_map.keys()), "y": counts}
    sns.barplot(x="x", y="y", data=data)
    plt.savefig("plot.png")


def get_response(rate):
    if rate <= 5 and rate > 0:
        print(
            "People are eagar to go offline yet no true pediction can still be made as the number is negligible and can also be significantly influenced by goverment's decision as well. The economic activity in this area has a recovers slightly faster, yet this can easily change if a strict lockdown is Imposed.\n So, offline services may consider ramping up their activity in this area."
        )
    elif rate >= -5 and rate < 0:
        print(
            "People are slightly so slowing down a bit more but this can change after goverment decision. The economic activity in this area has a slight less recovery rate, yet the situation might change if restrictions are lessened.\n So, ed-tech or online based services may consider ramping up their activity in this area."
        )
    elif rate == 0:
        print(
            "No exact prediction can be made at this point as the rate of slowdown and recover is the same and the government's decision may play a key role over here. The economic activity is in this area is recovering the same rate as it slowed down. Government decision is very crutial over here."
        )
    elif rate >= 5 and rate < 20:
        print(
            "People are slowly but stedily gettung back to normal as the Cases seem to slowly decrease and the restrictions also seem to slightly lessen. The economic activity in this area is recovering fast and the offline services should consider ramping up their effort as activities are again rejuvenating. "
        )
    elif rate <= -5 and rate > -20:
        print(
            "The rate of change indicates that the COVID cases are slowly increasing and more people are moving their work to home. The economic activity in this area is slowing down fast and the online services should consider ramping up their effort as offline activities are again shutting down. "
        )
    elif rate >= 20 and rate < 50:
        print(
            "The lockdown in this area has probably eased a bit as the people are showing more tendency to go out to work. The economic activity in this area is inscreasing a lot compared to the slowdown rate. Thus, People are considered to go out more and also take part in different activities more. So, Offline services may hope for a better outcome if new retrictions are not imposed."
        )
    elif rate <= -20 and rate > -50:
        print(
            "Many people still need to conduct activities from home and the locdown is getting more stricter then ever. The economic activity in the area can recover as significantly as they are slowed down by the pandemic. Thus, the offline activites might remain shut and business may boom for online business. "
        )
    elif rate >= 50 and rate < 100:
        print(
            "The things are going back to normal at a significnt pace as the restrictions have probably been lifted due to decreased number of cases. The economic activity in this area is significantly improving and it's not long for businesses to reopen. As the recovery rate more than or equal to 50%, online business may focus on ramping up their economic activities."
        )
    elif rate <= -50 and rate > -100:
        print(
            "Many People are still under lockdown due to Covid. The economic activity in this area is in decline and the existing lockdown is massively impacting the local businesses over there. Yet as most of the people are residing in their homw, it's a great opportunity for the online based service providing businesses to thrive in these circumstances."
        )
    elif rate >= 100:
        print(
            "Most of the People are already back to their daily offline activity. The Offline economic activity in this area is Booming and getting back to normal. So, It's a clear indication that the Offline businesses can soon go back to normal and investors in this area may continue investing in those businesses."
        )
    elif rate <= -100:
        print(
            "Significant Number of People are staying home. The economic activity in this area has signifinatly declined and is expected to decline more. Thus, investing in online service providing company is a very good option. As most of the people are staying at home they should be more and more inclined towards online services. So, online businesses are sure to boom during this time."
        )


if __name__ == "__main__":
    main()

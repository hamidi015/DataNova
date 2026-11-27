def segment_customers(df):

    young = len(df[df["Age"] <= 30])

    middle = len(
        df[(df["Age"] > 30) & (df["Age"] <= 50)]
    )

    senior = len(df[df["Age"] > 50])

    return {
        "Young": young,
        "Middle": middle,
        "Senior": senior
    }


def get_largest_segment(segments):

    return max(
        segments,
        key=segments.get
    )


def get_recommendation(segment):

    if segment == "Young":
        return (
            "Focus on digital, mobile, "
            "and social media marketing."
        )

    elif segment == "Middle":
        return (
            "Focus on loyalty programs "
            "and premium services."
        )

    else:
        return (
            "Focus on customer support "
            "and relationship building."
        )
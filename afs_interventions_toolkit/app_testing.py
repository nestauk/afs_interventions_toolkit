# Description: This is a testing file for the Parenting Intervention Survey.
import streamlit as st
from PIL import Image
import altair as alt
import numpy as np
import itertools

# import sys
# sys.path.append("..")
from afs_interventions_toolkit.getters.templates import get_template_data
from afs_interventions_toolkit.getters.dataframes import get_data
from afs_interventions_toolkit.getters.local_authorities import get_local_authorities
from afs_interventions_toolkit.getters.interventions import get_interventions
from afs_interventions_toolkit.utils.s3_saving import saving_to_s3
from afs_interventions_toolkit.utils.processing import process_string

# replace with ds_utils when the package is available
from utils.formatting import *
import streamlit as st
import pandas as pd

alt.themes.register("nestafont", nestafont)
alt.themes.enable("nestafont")
colours = NESTA_COLOURS


APP_TITLE = "Parenting Intervention Survey"


# icon to be used as the favicon on the browser tab
im = Image.open("afs_interventions_toolkit/images/favicon.ico")

# sets page configuration with favicon and title specified on line 4
st.set_page_config(page_title=APP_TITLE, layout="wide", page_icon=im)

header = st.container()
with header:
    # nesta logo
    nesta_logo = Image.open(f"afs_interventions_toolkit/images/nesta_logo.png")

    # set title of app to be title specified
    st.title(APP_TITLE)
    # Indicate that this dashboard is still a draft. Remove once final.
    st.markdown(
        "This dashboard is designed for Local Authorities to input their parenting interventions. The dashboard will provide a summary of the interventions through graphs and allow the user to download their data."
    )

tab1, tab2, tab3 = st.tabs(
    ["Inputting Parenting Interventions", "Figures", "Saving the data"]
)


with tab1:

    local_authorities = get_local_authorities()
    interventions_list = get_interventions()

    with st.form("Intervention Data Input"):

        # Local Authority
        local_authority = st.selectbox(
            "Select Local Authority",
            local_authorities["Local Authorities"],
            index=None,
            placeholder="Select or type a Local Authority",
        )

        try:
            councils_df = get_data("council/council_dataframe")
        except Exception as e:
            councils_df = get_template_data("council_dataframe")

        try:
            interventions_df = get_data(
                f"intervention/{process_string(local_authority)}"
            )
        except Exception as e:
            interventions_df = get_template_data("intervention_dataframe")

        # Percentage of children in each group
        st.write(
            "Please input the percentage of the children in each group. If you do not have the data, please leave the field blank."
        )
        percentage_universal = st.number_input(
            "Universal (%)",
            min_value=0,
            max_value=100,
            value=None,
            placeholder="Optional",
        )
        percentage_targeted = st.number_input(
            "Targeted (%)",
            min_value=0,
            max_value=100,
            value=None,
            placeholder="Optional",
        )
        percentage_targeted_plus = st.number_input(
            "Targeted Plus (%)",
            min_value=0,
            max_value=100,
            value=None,
            placeholder="Optional",
        )
        st.write("Please note that the sum of the percentages should be equal to 100.")

        st.write(
            "Now, please input information about the parenting intervention. If you have two interventions with the same name from the options, please input them as a custom intervention with different names to highlight the difference. Else they will be overwritten."
        )
        st.write(
            "If you have place information in both boxes it will combined the two."
        )

        # Intervention
        intervention_options = list(interventions_list["intervention"]) + [
            "Other"
        ]  # Replace with your intervention options

        intervention_choice = st.selectbox(
            "Select Intervention",
            intervention_options,
            index=None,
            placeholder="Select or type an intervention",
        )

        custom_intervention = st.text_input(
            "Custom Intervention",
            value="",
            max_chars=None,
            key=None,
            type="default",
            help=None,
            placeholder="Enter your own intervention",
        )

        # Age group
        ages = ["0-1", "1-2", "2-3", "3-4", "4-5", "5+"]
        ages_dict = {
            "0-1": [0, 1],
            "1-2": [1, 2],
            "2-3": [2, 3],
            "3-4": [3, 4],
            "4-5": [4, 5],
            "5+": [5],
        }
        age_group = st.multiselect(
            "Age Group", ages, placeholder="Select age groups for the intervention"
        )
        ages = [ages_dict[age] for age in age_group]
        age_group_values = list(set(itertools.chain(*ages)))

        # Target Population
        targets = ["Universal", "Targeted", "Targeted Plus", "Other"]
        target_population = st.selectbox(
            "What is the target population?",
            targets,
            index=None,
            placeholder="Select or type a target population",
        )

        # Geographically targeted

        binary = ["Yes", "No"]

        geographically_targeted = st.selectbox(
            "Is the intervention targeted geographically?",
            binary,
            index=None,
            placeholder="Select if the intervention is geographically targeted",
        )

        # Percentage of the council area

        percentage_council = st.number_input(
            "If yes, approximately what percentage of the council area?",
            min_value=0,
            max_value=100,
            value=None,
            placeholder="Optional",
        )

        # Referral route

        referral_options = [
            "Midwifery",
            "Health visiting",
            "Children's centre or Family Hub",
            "Early help, social work",
            "Education",
            "Voluntary partner",
            "Other",
        ]

        referral_route = st.multiselect(
            "Select Referral Route",
            referral_options,
            placeholder="Select or type a referral route",
        )

        custom_referral = st.text_input(
            "If other is selected, please input referral routes",
            value="",
            max_chars=None,
            placeholder="Please input if known",
        )

        # Children referred

        children_referred = st.number_input(
            "Number of children referred",
            min_value=0,
            max_value=None,
            value=None,
            placeholder="Please input if known",
        )

        # Children engaged

        children_engaged = st.number_input(
            "Number of children engaged",
            min_value=0,
            max_value=None,
            value=None,
            placeholder="Please input if known",
        )

        # Children who complete intervention

        children_completed = st.number_input(
            "Number of children who completed the intervention",
            min_value=0,
            max_value=None,
            value=None,
            placeholder="Please input if known",
        )

        # Primary Outcome

        outcomes = [
            "Improve parenting / adult-child relationship"
            "Improve adult-child relationship / attachment",
            "Improve home learning environment",
            "Improve children's cognitive development / language, communication, or literacy",
            "Improve children's socio-emotional development",
            "Improve child behaviour",
            "Improve children's physical health",
            "Improve children's mental health",
            "Support breastfeeding / infant feeding",
            "Improve birthing experience",
            "Improve relationship",
            "Support new parents",
            "Support parental mental health",
            "Provide school readiness support",
            "Provide adult alcohol and substance dependency support",
            "Other",
        ]
        primary_outcome = st.selectbox(
            "Select Primary Outcome",
            outcomes,
            index=None,
            placeholder="Select or type a primary outcome",
        )

        custom_outcome = st.text_input(
            "If other is selected, please input primary outcome",
            value="",
            max_chars=None,
            placeholder="Please input if known",
        )

        # Secondary outcomes

        secondary_outcomes = st.multiselect(
            "Select Secondary Outcomes",
            outcomes,
            placeholder="Select or type a secondary outcome",
        )

        custom_secondary_outcome = st.text_input(
            "If other is selected, please input secondary outcome",
            value="",
            max_chars=None,
            placeholder="Please input if known",
        )

        # Delivery Provider

        provider_options = [
            "Public Sector",
            "Private Sector",
            "Charity",
            "NHS",
            "Council",
            "Other",
        ]
        provider_choice = st.selectbox(
            "Select Delivery Provider",
            provider_options,
            index=None,
            placeholder="Select or type a delivery provider",
        )

        custom_provider = st.text_input(
            "If other is selected, please input provider",
            value="",
            max_chars=None,
            placeholder="Please input if known",
        )

        # Delivery Setting

        setting_options = [
            "Online",
            "Home",
            "Children's centre or equivalent",
            "Primary school",
            "Secondary School",
            "Sixth-form college or FE college",
            "Community Centre",
            "In-patient health setting",
            "Outpatient health setting",
            "Other",
        ]

        setting_choice = st.multiselect(
            "Select Delivery Setting",
            setting_options,
            placeholder="Select or type a delivery setting",
        )

        custom_setting = st.text_input(
            "If other is selected, please input setting",
            value="",
            max_chars=None,
            placeholder="Please input if known",
        )

        # Funder

        funder_options = ["Charity", "NHS", "Schools", "Council", "Other"]
        funder_choice = st.selectbox(
            "Select Funder",
            funder_options,
            index=None,
            placeholder="Select or type a funder",
        )

        custom_provider = st.text_input(
            "If other is selected, please input funder",
            value="",
            max_chars=None,
            placeholder="Please input if known",
        )

        # Annual Funding Amount

        annual_funding = st.number_input(
            "Annual Funding Amount",
            min_value=0,
            max_value=None,
            value=None,
            placeholder="Please input if known",
        )

        # Submit button
        submitted = st.form_submit_button("Add parenting intervention")

        if submitted:
            # Take the intervention choice if it is not empty or other, otherwise take the custom intervention
            intervention = (
                intervention_choice + " " + custom_intervention
                if intervention_choice not in ["Other", None] and custom_intervention
                else intervention_choice if intervention_choice else custom_intervention
            )

            # Take the referral choice and only combine the custom referral if one of the choices is "Other"
            referral = (
                referral_route + [custom_referral]
                if "Other" in referral_route
                else referral_route
            )
            # Drop "Other" if it is in the list
            referral = [x for x in referral if x != "Other"]

            # Take the primary outcome choice if it is not empty or other, otherwise take the custom primary outcome
            primary = (
                primary_outcome
                if primary_outcome not in ["Other", None]
                else custom_outcome
            )

            # Take the secondary outcomes and only combine the custom outcome if one of the choices is "Other"
            secondary = (
                secondary_outcomes + [custom_secondary_outcome]
                if "Other" in secondary_outcomes
                else secondary_outcomes
            )
            # Drop "Other" if it is in the list
            secondary = [x for x in secondary if x != "Other"]

            # Take the provider choice if it is not empty, otherwise take the custom provider
            provider = (
                provider_choice
                if provider_choice not in ["Other", None]
                else custom_provider
            )

            # Take the setting choice and only combine the custom outcome if one of the choices is "Other"
            setting = (
                setting_choice + [custom_setting]
                if "Other" in setting_choice
                else setting_choice
            )
            # Drop "Other" if it is in the list
            setting = [x for x in setting if x != "Other"]

            # Take the funder choice if it is not empty, otherwise take the custom funder
            funder = (
                funder_choice
                if funder_choice not in ["Other", None]
                else custom_provider
            )

            # Add the intervention to the interventions dataframe
            intervention_new_row = pd.DataFrame(
                {
                    "Council name": local_authority,
                    "Intervention name": intervention,
                    "Age group": str(age_group_values),
                    "Target population": target_population,
                    "Geographically targeted": geographically_targeted,
                    "Percentage of the council area": percentage_council,
                    "Referral route": str(referral),
                    "Children referred": children_referred,
                    "Children engaged": children_engaged,
                    "Children who complete intervention": children_completed,
                    "Primary outcome": primary,
                    "Secondary outcomes": str(secondary),
                    "Delivery provider": provider,
                    "Delivery setting": str(setting),
                    "Funder": funder,
                    "Annual funding amount": annual_funding,
                },
                index=[0],
            )

            # If the intervention is not in the dataframe, add it
            if intervention not in interventions_df["Intervention name"].values:
                interventions = pd.concat(
                    [interventions_df, intervention_new_row], axis=0, ignore_index=True
                )
            else:
                # Replace the row with the new row
                interventions = interventions_df[
                    interventions_df["Intervention name"] != intervention
                ]
                interventions = pd.concat(
                    [interventions, intervention_new_row], axis=0, ignore_index=True
                )

            saving_to_s3(
                interventions, f"intervention/{process_string(local_authority)}"
            )

            # Add row to council dataframe using pandas
            council_new_row = pd.DataFrame(
                {
                    "Council Name": local_authority,
                    "Percentage in each group: Universal": (
                        percentage_universal
                        if not None
                        else councils_df.loc[
                            councils_df["Council Name"] == local_authority,
                            "Percentage in each group: Universal",
                        ]
                    ),
                    "Percentage in each group: Targeted": (
                        percentage_targeted
                        if not None
                        else councils_df.loc[
                            councils_df["Council Name"] == local_authority,
                            "Percentage in each group: Targeted",
                        ]
                    ),
                    "Percentage in each group: Targeted Plus": (
                        percentage_targeted_plus
                        if not None
                        else councils_df.loc[
                            councils_df["Council Name"] == local_authority,
                            "Percentage in each group: Targeted Plus",
                        ]
                    ),
                    "Number of interventions": interventions.shape[0],
                },
                index=[0],
            )

            # If the council is not in the dataframe, add it
            if local_authority not in councils_df["Council Name"].values:
                councils_df = pd.concat(
                    [councils_df, council_new_row], axis=0, ignore_index=True
                )
            else:
                # Replace the row with the new row
                councils_df = councils_df[
                    councils_df["Council Name"] != local_authority
                ]
                councils_df = pd.concat(
                    [councils_df, council_new_row], axis=0, ignore_index=True
                )

            saving_to_s3(councils_df, "council/council_dataframe")

            st.success("Intervention added successfully!")

    # [TESTING]
    try:
        updated_councils = get_data("council/council_dataframe")
        st.dataframe(updated_councils)
    except Exception as e:
        st.write("No council added yet")

    try:
        updated_intervention = get_data(
            f"intervention/{process_string(local_authority)}"
        )
        st.dataframe(updated_intervention)
    except Exception as e:
        st.write("No interventions added yet")

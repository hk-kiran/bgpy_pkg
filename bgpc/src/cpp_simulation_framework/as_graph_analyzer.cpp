#include "announcement.hpp"
#include "as.hpp"
#include "cpp_simulation_engine.hpp"
#include "as_graph_analyzer.hpp"


ASGraphAnalyzer::ASGraphAnalyzer(std::shared_ptr<CPPSimulationEngine> engine,
                             const std::vector<std::string>& ordered_prefixes,
                             const std::unordered_set<int>& victim_asns,
                             const std::unordered_set<int>& attacker_asns)
    : engine(engine),
      victim_asns(victim_asns),
      attacker_asns(attacker_asns) {
    for (auto& as_obj_pair : engine->as_graph->as_dict) {
        auto& as_obj = as_obj_pair.second;
        most_specific_ann_dict[as_obj->asn] = get_most_specific_ann(as_obj, ordered_prefixes);
    }
}

std::unordered_map<int, std::unordered_map<int, Outcomes>> ASGraphAnalyzer::analyze() {
    for (auto& as_obj_pair : engine->as_graph->as_dict) {
        auto as_obj = as_obj_pair.second; // Assuming as_graph is a map from IDs to AS shared_ptrs

        // Data Plane Analysis
        Outcomes data_outcome = get_as_outcome_data_plane(as_obj);
        data_plane_outcomes[as_obj->asn] = data_outcome;

        // Control Plane Analysis
        Outcomes ctrl_outcome = get_as_outcome_ctrl_plane(as_obj);
        control_plane_outcomes[as_obj->asn] = ctrl_outcome;
    }

    // Using integer values from the Plane enum as keys
    outcomes[static_cast<int>(Plane::DATA)] = data_plane_outcomes;
    outcomes[static_cast<int>(Plane::CTRL)] = control_plane_outcomes;
    return outcomes;
}


std::optional<std::shared_ptr<Announcement>> ASGraphAnalyzer::get_most_specific_ann(std::shared_ptr<AS> as_obj, const std::vector<std::string>& ordered_prefixes) {
    for (const auto& prefix : ordered_prefixes) {
        std::shared_ptr<Announcement> most_specific_ann = as_obj->policy->localRIB.get_ann(prefix);
        if (most_specific_ann) {
            return most_specific_ann;
        }
    }
    return std::nullopt;  // Return empty optional if no announcement is found
}

Outcomes ASGraphAnalyzer::get_as_outcome_data_plane(std::shared_ptr<AS> as_obj) {
    // Check if the outcome is already determined for the AS
    auto it = data_plane_outcomes.find(as_obj->asn);
    if (it != data_plane_outcomes.end()) {
        return it->second;
    }

    // Get the most specific announcement for the AS
    std::optional<std::shared_ptr<Announcement>> most_specific_ann = most_specific_ann_dict[as_obj->asn];

    // Determine the outcome based on the most specific announcement
    Outcomes outcome = determine_as_outcome_data_plane(as_obj, most_specific_ann);

    // Handle undetermined cases, potentially involving recursion
    if (outcome == Outcomes::UNDETERMINED && most_specific_ann) {
        auto next_as = engine->as_graph->as_dict[(*most_specific_ann)->as_path[1]]; // Example of getting the next AS in the path
        outcome = get_as_outcome_data_plane(next_as); // Recursively determine the outcome
    }

    assert(outcome != Outcomes::UNDETERMINED); // Ensure that the outcome is no longer undetermined

    // Store and return the determined outcome
    data_plane_outcomes[as_obj->asn] = outcome;
    return outcome;
}

Outcomes ASGraphAnalyzer::determine_as_outcome_data_plane(std::shared_ptr<AS> as_obj, std::optional<std::shared_ptr<Announcement>> most_specific_ann) {
    // Check if the AS is an attacker
    if (attacker_asns.find(as_obj->asn) != attacker_asns.end()) {
        return Outcomes::ATTACKER_SUCCESS;
    }

    // Check if the AS is a victim
    if (victim_asns.find(as_obj->asn) != victim_asns.end()) {
        return Outcomes::VICTIM_SUCCESS;
    }

    // Check if there is no announcement or other specific conditions are met
    if (!most_specific_ann ||
        (*most_specific_ann)->as_path.size() == 1 ||
        (*most_specific_ann)->recv_relationship == Relationships::ORIGIN ||
        (*most_specific_ann)->traceback_end) {
        return Outcomes::DISCONNECTED;
    }

    // If none of the above conditions are met, the outcome is undetermined
    return Outcomes::UNDETERMINED;
}

Outcomes ASGraphAnalyzer::get_as_outcome_ctrl_plane(std::shared_ptr<AS> as_obj) {
    // Check if the outcome is already computed for the AS
    auto it = control_plane_outcomes.find(as_obj->asn);
    if (it != control_plane_outcomes.end()) {
        return it->second;
    }

    // Get the most specific announcement for the AS
    std::optional<std::shared_ptr<Announcement>> most_specific_ann = most_specific_ann_dict[as_obj->asn];

    // Determine the outcome based on the most specific announcement
    Outcomes outcome = determine_as_outcome_ctrl_plane(as_obj, most_specific_ann);

    // Store and return the determined outcome
    control_plane_outcomes[as_obj->asn] = outcome;
    return outcome;
}

Outcomes ASGraphAnalyzer::determine_as_outcome_ctrl_plane(std::shared_ptr<AS> as_obj, std::optional<std::shared_ptr<Announcement>> ann) {
    // If there is no announcement, the AS is considered disconnected in the control plane
    if (!ann) {
        return Outcomes::DISCONNECTED;
    }

    // Check if the origin of the announcement is an attacker
    if (attacker_asns.find((*ann)->origin()) != attacker_asns.end()) {
        return Outcomes::ATTACKER_SUCCESS;
    }

    // Check if the origin of the announcement is a victim
    if (victim_asns.find((*ann)->origin()) != victim_asns.end()) {
        return Outcomes::VICTIM_SUCCESS;
    }

    // If none of the above conditions are met, the AS is considered disconnected
    // This can be adjusted based on more specific rules for your scenario
    return Outcomes::DISCONNECTED;
}

Outcomes ASGraphAnalyzer::get_other_as_outcome_hook(std::shared_ptr<AS> as_obj) {
    // Used to satisfy type checker, hook method for other metrics
    return Outcomes::ATTACKER_SUCCESS;
}
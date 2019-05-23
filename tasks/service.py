def filter_tags(tags_by_task):
    tags_list = []
    for list_tag in tags_by_task:
        for tag in list_tag:
            if tag not in tags_list:
                tags_list.append(tag)
    return tags_list

def filter_tasks(tasks, tag):
    list_found_tasks = []
    for dic in tasks:
        if tag in dic["tags"]:
            list_found_tasks.append(dic["task_id"])
    return list_found_tasks         

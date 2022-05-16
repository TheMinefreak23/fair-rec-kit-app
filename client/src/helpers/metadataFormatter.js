/*This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)*/

export function formatMetadata(metadata){
    var tabs = 0
    for(var i = 0; i < metadata.length; i++){
        switch(metadata[i]){
            case '{':
            case '[':
                tabs++
                metadata = insert(metadata, '\n'+('\t'.repeat(tabs)), i+1)
                break;
            case '}':
            case ']':
                tabs--
                metadata = insert(metadata, '\n'+('\t'.repeat(tabs)), i)
                i = i + 1 + tabs //jump the counter forward to not get caught in an infinite loop of checking the same closing bracket
                break;
            case ',':
                metadata = insert(metadata, '\n'+('\t'.repeat(tabs)), i+1)
        }
    }
    return metadata
}

/**
 * inserts a string into another at the specified position
 * @param {string} string string that will be inserted into
 * @param {string} insert string that will be inserted
 * @param {int} position where the insertion will take place
 * @returns {string}
 */
export function insert(string, insert, position){
    return [string.slice(0, position), insert, string.slice(position)].join('')
}
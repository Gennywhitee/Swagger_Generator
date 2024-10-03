@Entity
@Table(name="user_feed")
public class User implements Serializable {

    @Id
    @Column(name="user_id")
    private long userId;

    @Column(name="is_repost")
    private boolean isRepost;

    @Column(name="date_created")
    private Date dateCreated;

    @OneToOne
    @JoinColumn(name="amici")
    private Friend friend;

}

